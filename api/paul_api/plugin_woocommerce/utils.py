#!/usr/bin/env python3

import copy
import datetime
import json
import os
import re
import sys
import traceback
import urllib
from dataclasses import dataclass, field
from pprint import pprint
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    Iterable,
    List,
    Optional,
    Tuple,
    TypeVar,
    Union,
)
from urllib import parse

import requests
from api import models
from django.contrib.auth.models import User
from django.utils import timezone
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError
from requests.packages.urllib3.util.retry import Retry

from .table_fields import (
    CUSTOMER_FIELDS,
    ORDERS_COMPACT_FIELDS,
    ORDERS_VERBOSE_FIELDS,
    SUBSCRIPTIONS_FIELDS,
)

T = TypeVar("T")


DEFAULT_TIMEOUT = 20  # seconds


@dataclass
class Msg(Exception):
    msg: str

    def to_str(self) -> str:
        return f"Error: {self.msg}\nPlease try the action again. If the error persists contact support"


def err_url_get(url: str, err: HTTPError) -> Msg:
    return Msg(f"GET on URL {url} returned {err}")


def err_url_no_json(url: str) -> Msg:
    return Msg(f"GET on {url} did not return a valid JSON")


def err_url_response_code(url: str, code) -> Msg:
    return Msg(f"URL {url} returned unexpected code {code}")


def err_fallback(msg: str) -> Msg:
    return Msg(f"Unexpected migration error: {msg}")


def err_transform(table: str, row: Any, column: str, err: Any) -> Msg:
    sep = ": " if err else ""
    return Msg(
        f"Encountered error for column {column} of entry Id {row} in table {table}{sep}{err}. Value left empty"
    )


# pair of (data,messages) returned by transform functions
TransformResult = Tuple[List[Dict[str, Any]], List[Msg]]


@dataclass
class Endpoint:
    name: str
    version: str

    mk_url: Callable[
        ["Endpoint", str, int], str
    ] = lambda self, base_url, page: f"{base_url}{self.version}/{self.name}?page={page}"
    filter: Callable[[Any], bool] = lambda _entry: True

    # dict of suffix -> transform
    transform: Dict[str, Callable[[List], TransformResult]] = field(
        default_factory=dict
    )


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs) -> None:
        self.timeout = DEFAULT_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


class Fetcher:
    def __init__(self, key: str, secret: str) -> None:
        self.key = key
        self.secret = secret
        self.http = requests.Session()

        retries = Retry(
            total=10, backoff_factor=4, status_forcelist=[429, 500, 502, 503, 504]
        )

        # mount timeout adapter so that all calls have the same timeout
        adapter = TimeoutHTTPAdapter(timeout=60, max_retries=retries)
        self.http.mount("https://", adapter)
        self.http.mount("http://", adapter)

        # the request will raise an exception on 4XX and 5XX
        assert_status_hook = (
            lambda response, *args, **kwargs: response.raise_for_status()
        )
        self.http.hooks["response"] = [assert_status_hook]

    def get(self, url: str, user_params: Dict[str, str] = {}):
        # print(f"requesting {url}")
        params = {
            "consumer_key": self.key,
            "consumer_secret": self.secret,
            **user_params,
        }
        response = self.http.get(url, params=params)

        return response

    def get_json(
        self, url, user_params: Dict[str, str] = {}
    ) -> Union[None, List, Dict]:
        try:
            response = self.get(url, user_params)
            if response.status_code == requests.codes.no_content:
                return None
            if response.status_code != requests.codes.ok:
                raise err_url_response_code(url, response.status_code)
            return response.json()
        except HTTPError as err:
            raise err_url_get(url, err) from err
        except ValueError as err:
            raise err_url_no_json(url) from err


def fix_date_format(d: str) -> str:
    if not d:
        return ""
    return datetime.datetime.strptime(d, "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d")


def _key(key_name: str, default: Optional[T] = None) -> Callable[[Dict[str, Any]], T]:
    if default is None:
        return lambda obj: obj[key_name]
    return lambda obj: obj.get(key_name, default)


CUSTOMER_METADATA_KEYS = {
    "Newsletter comunitate": lambda obj: (obj or {})
    .get("_mailchimp_sync_status", {})
    .get("status")
    == "subscribed",
    "Mailchimp WooCommerce subscribed": lambda obj: str(
        obj.get("mailchimp_woocommerce_is_subscribed")
    )
    == "1",
    "Mailchimp opt in": lambda obj: str(
        obj.get("_wc_memberships_mailchimp_sync_opt_in")
    )
    == "yes",
}


def add_columns(
    entry: Dict[str, Any],
    entry_id: Any,
    table: str,
    cols: Dict[str, Callable],
    src: Dict[str, Any],
) -> List[Msg]:
    messages = []
    for col_name, get_val in cols.items():
        v = ""
        try:
            v = get_val(src)
        except KeyError as err:
            messages.append(err_transform(table, entry_id, col_name, err))
        except Exception as ex:
            messages.append(err_transform(table, entry_id, col_name, str(ex)))

        entry[col_name] = v
    return messages


def transform_customers(data: List) -> TransformResult:
    COLUMNS = {
        "ID Client": _key("id"),
        "Nume": lambda obj: f"{obj['first_name']} {obj['last_name']}".strip(),
        "Email": _key("email"),
    }

    BILLING_COLUMNS = {
        "Email": _key("email"),
        "Companie": _key("company"),
        "Adresa": lambda obj: f"{obj['address_1']} {obj['address_2']}".strip(),
        "Tara": _key("country"),
        "Judet": _key("state"),
        "Oras": _key("city"),
        "Cod postal": _key("postcode"),
        "Telefon": _key("phone"),
    }

    customers = []
    messages = []

    for cust in data:
        try:
            cust_id = cust.get("id")
            entry: Dict[str, Any] = {}
            # name: get_val(cust) for name, get_val in COLUMNS.items()}
            messages += add_columns(entry, cust_id, "customers", COLUMNS, src=cust)

            billing = cust["billing"]
            messages += add_columns(
                entry, cust_id, "customers", BILLING_COLUMNS, src=billing
            )

            messages += add_columns(
                entry,
                cust_id,
                "customers",
                CUSTOMER_METADATA_KEYS,
                src={md["key"]: md["value"] for md in cust["meta_data"]},
            )

            customers.append(entry)

        except Exception as err:
            messages.append(err_fallback(f"transform error for customer: {err}"))

    return customers, messages


def fetch_items_with_ids(fetcher, ids, mk_url) -> Tuple[Dict[str, Any], List[Msg]]:
    """
    returns messages
    """
    messages = []
    items = {}
    for ID in ids:
        url = mk_url(ID)
        try:
            resp_json = fetcher.get_json(url)
        except Msg as msg:
            messages.append(msg)
            continue
        except Exception as err:
            messages.append(err_fallback(f"get error for url {url}: {err}"))
            continue
        items[str(ID)] = resp_json

    return items, messages


def fetch_subscription_notes(
    fetcher, base_url, subscription_ids
) -> Tuple[Dict[str, Any], List[Msg]]:
    return fetch_items_with_ids(
        fetcher, subscription_ids, lambda ID: f"{base_url}v1/subscriptions/{ID}/notes"
    )


def fetch_customers_by_id(
    fetcher, base_url, customer_ids
) -> Tuple[Dict[str, Any], List[Msg]]:
    return fetch_items_with_ids(
        fetcher, customer_ids, lambda ID: f"{base_url}v3/customers/{ID}"
    )


def fetch_customers_by_email(
    fetcher, base_url, emails: List[str]
) -> Tuple[Dict[str, Any], List[Msg]]:
    """
    emails are sometimes emails, sometimes a "Name (email)" combo.
    First we try to parse the email out, and only request with the full string as fallback.
    The keys in the returned dict are the original strings (so they can be looked up from subscriptions)
    """
    messages = []
    customers_by_email = {}
    for email in emails:

        api_tries = [email]
        if "(" in email:
            # probably a "Name (email)" string
            pieces = re.split("\(|\)", email)
            # api_tries.insert(0, pieces[1])
            api_tries = [pieces[1]]

        resp_json = None
        for attempt in api_tries:
            arg = urllib.parse.quote(attempt)
            url = f"{base_url}v3/customers/?role=all&email={arg}"
            try:
                resp_json = fetcher.get_json(url)
                # print(f"resp_json: {json.dumps(resp_json)}")
                if resp_json:
                    break
            except Msg as msg:
                messages.append(msg)
                continue
            except Exception as err:
                messages.append(err_fallback(f"get error for email {email}: {err}"))
                continue
        else:
            # not_found += api_tries
            continue
        # print(res)
        # print(json.dumps(res.json(), indent=4))
        customers_by_email[email] = resp_json

    # print("emails not found", not_found)
    # sys.exit(0)
    return customers_by_email, messages


def is_gift(sub: Dict) -> Optional[str]:
    """
    returns None when it's not a gift, and returns the meta value when it is
    """
    items = sub.get("line_items")
    if not isinstance(items, list):
        return None
    for item in items:
        meta = item.get("meta")
        if not isinstance(meta, list):
            continue
        for meta_item in meta:
            if meta_item.get("key") == "wcsg_recipient":
                return meta_item["value"]

    if any("cadou" in item["name"].lower() for item in items):
        return sub["billing"]["email"]
    return None


def partition_emails_and_customer_ids(
    subscriptions_data: List,
) -> Tuple[List[str], List[str]]:
    """
    returns a tuple of (emails, cust_ids)
    """
    emails = []
    cust_ids = []
    for sub in subscriptions_data:
        gift_mail = is_gift(sub)
        if gift_mail:
            emails.append(gift_mail)
        else:
            cust_ids.append(str(sub["customer_id"]))
    return emails, cust_ids


def fetch_convoluted_data_stage_2(
    fetcher: Fetcher,
    base_url: str,
    subs_ep: Endpoint,
    notes_fname: str,
    customers_emails_fname: str,
) -> List[Msg]:
    messages = []
    subscriptions_data = get_json(first_file(subs_ep))

    subscription_notes, new_msgs = fetch_subscription_notes(
        fetcher, base_url, [sub["id"] for sub in subscriptions_data]
    )
    put_json(notes_fname, subscription_notes)
    messages += new_msgs

    emails, _cust_ids = partition_emails_and_customer_ids(subscriptions_data)

    # print("mails :", len(emails))
    # print(emails)

    customers_by_email, customer_msgs = fetch_customers_by_email(
        fetcher, base_url, emails
    )
    put_json(customers_emails_fname, customers_by_email)
    messages += customer_msgs
    return messages


def fetch_convoluted_data_stage_3(
    fetcher: Fetcher,
    base_url: str,
    subs_ep: Endpoint,
    memberships_lifetime_ep: Endpoint,
    memberships_old_ep: Endpoint,
    customers_emails_fname: str,
    known_customers,
    customers_fname: str,
) -> List[Msg]:
    subscriptions_data = get_json(first_file(subs_ep))
    life_members_data = get_json(first_file(memberships_lifetime_ep))
    old_members_data = get_json(first_file(memberships_old_ep))
    customers_by_email = get_json(customers_emails_fname)

    ids_from_email = set(
        str(entry["id"]) for c in customers_by_email.values() for entry in c
    )

    known_customer_ids = set(known_customers.keys())

    ids_from_life_members = set(str(m["customer_id"]) for m in life_members_data)
    ids_from_old_members = set(str(m["customer_id"]) for m in old_members_data)

    _emails, cust_ids = partition_emails_and_customer_ids(subscriptions_data)
    cust_ids_set = set(cust_ids)

    new_ids_from_email = ids_from_email - known_customer_ids
    # print("new from email", list(sorted(new_ids_from_email)))
    new_ids_from_life = ids_from_life_members - known_customer_ids
    # print("new from life", list(sorted(new_ids_from_life)))
    new_ids_from_old = ids_from_old_members - known_customer_ids
    # print("new from old", list(sorted(new_ids_from_old)))
    new_ids_from_subs = cust_ids_set - known_customer_ids
    # print("new from subs", list(sorted(new_ids_from_subs)))

    all_cust_ids = (
        list(cust_ids_set)
        + list(ids_from_email)
        + list(ids_from_life_members)
        + list(ids_from_old_members)
    )

    # print("cust_ids :", len(cust_ids))
    # print(cust_ids)

    all_cust_ids_set = set(all_cust_ids)
    remaining_ids = all_cust_ids_set - set(known_customers.keys())
    # print("REMAINING: ", list(sorted(remaining_ids)))
    # print("REMAINING: ", len(cust_ids))

    # print("cust_ids :", len(cust_ids))
    # print(cust_ids)

    customers_by_id, messages = fetch_customers_by_id(fetcher, base_url, remaining_ids)
    customers_by_id.update(known_customers)
    put_json(customers_fname, customers_by_id)
    return messages


def filter_for_prefix_and_strip(
    iter: Iterable[str], prefix: str
) -> Generator[str, None, None]:
    for x in iter:
        if not x:
            continue
        if x.startswith(prefix):
            yield x.split(prefix)[1]


def transform_convoluted(
    subscriptions_data,
    life_members_data,
    old_members_data,
    subscription_notes,
    customers_by_id,
    customers_by_email,
) -> TransformResult:

    USER_DATA_COLUMNS = {
        "Adresa": lambda obj: f"{obj['address_1']} {obj['address_2']}".strip(),
        "Cod postal": _key("postcode"),
        "Judet": _key("state"),
        "Oras": _key("city"),
        "Tara": _key("country"),
        "Companie": _key("company"),
    }

    BILLING_COLUMNS = {
        **USER_DATA_COLUMNS,
        "Telefon": _key("phone", ""),
    }

    def compute_recurrence(sub: Dict) -> str:
        # just in case it's either string or int
        billing_interval = str(sub["billing_interval"])
        billing_period = sub["billing_period"]
        if billing_interval == "1" and billing_period == "year":
            return "Anual"
        elif billing_interval == "1" and billing_period == "month":
            return "Lunar"

        return f"Every {billing_interval} {billing_period}"

    def status_value(obj: Dict) -> str:
        st = obj["status"]
        if st == "paused":
            return "on hold"
        return st

    COMMON_COLUMNS = {
        "Data abonarii": lambda obj: fix_date_format(obj["start_date"]),
        "Data expirarii": lambda obj: fix_date_format(obj["end_date"]),
        "Data urmatoarei plati": lambda obj: fix_date_format(
            obj.get("next_payment_date", "")
        ),
        "ID abonament": _key("id"),
        "Metoda de plata": _key("payment_method", ""),
        "Status": status_value,
        "Total": _key("total", ""),
    }

    abonamente = []
    messages = []

    for sub in subscriptions_data:
        if not sub.get("line_items"):
            continue

        entry: Dict[str, Any] = {}
        sub_id = sub.get("id")

        try:
            messages += add_columns(
                entry, sub_id, "abonamente", COMMON_COLUMNS, src=sub
            )
            entry["Creat via"] = sub["created_via"]
            entry["Recurenta"] = compute_recurrence(sub)

            gift_mail = is_gift(sub)
            if gift_mail:
                cust_id = customers_by_email[gift_mail][0]["id"]
            else:
                cust_id = sub["customer_id"]

            if str(cust_id) == "0":
                continue

            cust = customers_by_id[str(cust_id)]

            entry["Nume"] = f"{cust['first_name']} {cust['last_name']}".strip()
            entry["Email"] = cust["email"]
            messages += add_columns(
                entry,
                sub_id,
                "abonamente",
                CUSTOMER_METADATA_KEYS,
                src={md["key"]: md["value"] for md in cust["meta_data"]},
            )
            entry["Cadou"] = "Yes" if gift_mail else "No"

            if gift_mail:
                billing = cust["billing"]
            else:
                billing = sub["billing"]

            messages += add_columns(
                entry,
                sub_id,
                "abonamente",
                BILLING_COLUMNS,
                src=billing,
            )

            items = sub["line_items"]

            # convert outlier cases to regular ones
            if len(items) == 2:
                items = [copy.deepcopy(items[0])]

            elif len(items) == 6:
                # assumed to be test cases
                continue

            if len(items) == 1:
                item_name = items[0]["name"]
                quantity = items[0]["quantity"]

            elif len(items) == 5:
                item_name = items[0]["name"]
                quantity = items[0]["quantity"]

                other_names = set(i["name"] for i in items[1:])
                other_qty = [i["quantity"] for i in items[1:]]

                EXPECTED_SETS = (
                    {"DoR #38", "DoR #39", "DoR #40", "DoR #41"},
                    {"DoR #39", "DoR #40", "DoR #41", "DoR #42"},
                )
                assert other_names in EXPECTED_SETS, f"wrong {other_names}"
                assert other_qty == [quantity] * 4
            else:
                raise Exception(
                    f"unrecognized line_items pattern for subscription id {sub['id']}"
                )

            entry["Cantitate"] = quantity
            entry["Ce contine"] = item_name

            nume_abonament = None
            if gift_mail:
                for item in items:
                    if item["product_id"] == 27867:
                        nume_abonament = "Abonament Digital Lunar Cadou"
                        break
                    elif item["product_id"] in (60377, 27869):
                        nume_abonament = "Abonament Digital Cadou"
                        break
                    elif item["product_id"] == 28702:
                        nume_abonament = "Abonament Digital + Print Anual Cadou"
                        break
                else:
                    messages.append(
                        err_transform(
                            "abonamente",
                            sub_id,
                            "Nume abonament",
                            "unmatched gift product id in items",
                        )
                    )
            else:
                for item in items:
                    if item["product_id"] == 27867:
                        nume_abonament = "Abonament Digital Lunar"
                        break
                    elif item["product_id"] == 27869:
                        nume_abonament = "Abonament Digital Anual"
                        break
                    elif item["product_id"] == 28702:
                        nume_abonament = "Abonament Digital + Print Anual"
                        break
                else:
                    messages.append(
                        err_transform(
                            "abonamente",
                            sub_id,
                            "Nume abonament",
                            "unmatched product id in items",
                        )
                    )

            entry["Nume abonament"] = nume_abonament

            sub_notes = subscription_notes[str(sub["id"])]

            delivery_note = next(
                filter_for_prefix_and_strip(
                    (note["note"] for note in sub_notes), "delivery: "
                ),
                "",  # default
            )
            entry["Metoda de livrare"] = delivery_note

            entry["Note"] = " ".join(
                filter_for_prefix_and_strip(
                    (note["note"] for note in sub_notes), "note: "
                )
            )

            abonamente.append(entry)

        except Exception as e:
            messages.append(
                err_fallback(
                    f"exception for subscription {sub_id} : {str(type(e))} {e}"
                )
            )
            # traceback.print_exc(file=sys.stderr)
            continue

    reference_keys = list(sorted(abonamente[0].keys()))

    for old in old_members_data:
        if str(old.get("customer_id")) == "0":
            continue

        try:
            entry, new_msg = abonament_entry_for_member_data(
                old, COMMON_COLUMNS, USER_DATA_COLUMNS, customers_by_id
            )
            entry["Nume abonament"] = "Abonament vechi"
            messages += new_msg

            assert (
                list(sorted(entry.keys())) == reference_keys
            ), f"columns missing for old membership {old.get('id')}"
            abonamente.append(entry)

        except Exception as e:
            messages.append(
                err_fallback(
                    f"exception for old membership {old.get('id')} : {str(type(e))} {e}"
                )
            )
            # traceback.print_exc(file=sys.stderr)
            continue

    for life in life_members_data:
        if str(life.get("customer_id")) == "0":
            continue

        try:
            entry, new_msg = abonament_entry_for_member_data(
                life, COMMON_COLUMNS, USER_DATA_COLUMNS, customers_by_id
            )
            entry["Nume abonament"] = "Abonament pe viata"
            messages += new_msg

            assert (
                list(sorted(entry.keys())) == reference_keys
            ), f"columns missing for lifetime membership {life.get('id')}"
            abonamente.append(entry)

        except Exception as e:
            messages.append(
                err_fallback(
                    f"exception for lifetime membership {life.get('id')} : {str(type(e))} {e}"
                )
            )
            # traceback.print_exc(file=sys.stderr)
            continue

    return abonamente, messages


# this would work nicer as an inner function, but python is acting too weird with captures here
def abonament_entry_for_member_data(
    mem,
    COMMON_COLUMNS: Dict[str, Callable],
    user_data_columns: Dict[str, Callable],
    customers_by_id,
) -> Tuple[Dict[str, Any], List[Msg]]:
    entry: Dict[str, Any] = {}
    sub_id = mem.get("id")
    messages = []
    messages += add_columns(entry, sub_id, "abonamente", COMMON_COLUMNS, src=mem)

    entry["Creat via"] = "admin"
    entry["Recurenta"] = ""
    entry["Ce contine"] = ""
    entry["Cadou"] = "No"

    cust_id = mem["customer_id"]

    # cust = customers_by_id.get(cust_id) or customers_by_id[str(cust_id)]
    cust = customers_by_id[str(cust_id)]
    customer_meta = {m["key"]: m["value"] for m in cust["meta_data"]}

    entry["Nume"] = f"{cust['first_name']} {cust['last_name']}".strip()
    entry["Email"] = cust["email"]
    messages += add_columns(
        entry,
        sub_id,
        "abonamente",
        CUSTOMER_METADATA_KEYS,
        src=customer_meta,
    )

    messages += add_columns(
        entry,
        sub_id,
        "abonamente",
        user_data_columns,
        src=cust["shipping"],
    )
    messages += add_columns(
        entry,
        sub_id,
        f"abonamente st={mem.get('status', 'None')}",
        {"Telefon": _key("shipping_phone", "")},
        src=customer_meta,
    )

    entry["Metoda de livrare"] = customer_meta.get("delivery_note")
    entry["Cantitate"] = int(customer_meta.get("print_quantity", 1))
    entry["Note"] = customer_meta.get("customer_note")

    return entry, messages


def transform_orders(data: List, distribute: bool) -> TransformResult:
    def infer_tip_comanda(obj) -> str:
        if obj["payment_method"] == "braintree_cc" and obj["created_via"] == "checkout":
            return "noua"
        if (
            obj["payment_method"] == "braintree_cc"
            and obj["created_via"] == "subscription"
        ):
            return "reinnoire"
        if (
            obj["payment_method"] == "sn_wc_mobilpay"
            and obj["created_via"] == "checkout"
        ):
            return "produs"
        return "manual"

    COLUMNS = {
        "ID Comanda": _key("number"),
        "Data": _key("date_created"),
        "Tip comanda": infer_tip_comanda,
        "Status": _key("status"),
    }

    BILLING_SHIPPING_COLUMNS = {
        "Nume": lambda obj: f"{obj['first_name']} {obj['last_name']}".strip(),
        "Email": _key("email", ""),  # not all entries have this key
        "Companie": _key("company"),
        "Adresa": lambda obj: f"{obj['address_1']} {obj['address_2']}".strip(),
        "Tara": _key("country"),
        "Judet": _key("state"),
        "Oras": _key("city"),
        "Cod Postal": _key("postcode"),
        "Telefon": _key("phone", ""),  # not all entries have this key
    }

    orders = []
    messages = []
    table_name = "orders_" + ("verbose" if distribute else "compact")

    for order in data:
        if "line_items" not in order or len(order["line_items"]) == 0:
            continue

        order_id = order.get("id")

        try:
            entry: Dict[str, Any] = {}
            messages += add_columns(entry, order_id, table_name, COLUMNS, src=order)
            entry["Data"] = fix_date_format(entry["Data"])

            billing = order["billing"]
            messages += add_columns(
                entry,
                order_id,
                table_name,
                cols={
                    name + " (facturare)": fn
                    for name, fn in BILLING_SHIPPING_COLUMNS.items()
                },
                src=billing,
            )

            shipping = order["shipping"]
            messages += add_columns(
                entry,
                order_id,
                table_name,
                cols={
                    name + " (livrare)": fn
                    for name, fn in BILLING_SHIPPING_COLUMNS.items()
                },
                src=shipping,
            )

            if not distribute:
                entry["Pret"] = order["total"]
                entry["Produse"] = ", ".join(
                    f"{item['quantity']} x {item['name']}"
                    for item in order["line_items"]
                )
                orders.append(entry)
            else:
                for item in order["line_items"]:
                    replica = copy.deepcopy(entry)
                    replica["Produs"] = item["name"]
                    replica["Cantitate"] = item["quantity"]
                    replica["Pret"] = str(
                        float(item["total"]) + float(item["total_tax"])
                    )
                    replica["ID Produs"] = f"{order['id']}_{item['id']}"
                    orders.append(replica)

        except Exception as e:
            messages.append(err_fallback(f"exception for order {order['id']} : {e}"))
            continue

    return orders, messages


def fetch_all(
    endpoints: List[Endpoint], fetcher, base_url: str
) -> Tuple[bool, List[Msg]]:
    """
    returns success (false if any endpoint had zero entries) and list of errors
    """
    messages = []
    success = True

    for ep in endpoints:
        count, ep_messages = fetch_one(ep, fetcher, base_url)
        success = success and count > 0
        messages += ep_messages

    return success, messages


def fetch_one(ep: Endpoint, fetcher, base_url: str) -> Tuple[int, List[Msg]]:
    """
    returns count of entries and list of errors
    """
    messages = []
    params = {"per_page": 100}

    # page = ep.get("page") or 1
    page = 1
    data: List = []

    mk_url = ep.mk_url

    while True:
        # if page == 48 or page == 57:
        #     page += 1
        #     continue
        if page % 500 == 0:
            with open(f"partial_{page}_{first_file(ep)}", "w") as f:
                f.write(json.dumps(data, indent=4))

        # mypy bug: https://github.com/python/mypy/issues/5485
        url = mk_url(ep, base_url, page)  # type: ignore

        try:
            response_json = fetcher.get_json(url, user_params=params)
        except Msg as msg:
            messages.append(msg)
            break
        except Exception as err:
            messages.append(err_fallback(f"{ep.version} {ep.name} {err}"))
            break

        # print(f"{ep_name}, page {page}:  {len(response_json)}")
        # print(f"json: {json.dumps(response_json, indent=4)}")
        # break

        if len(response_json) > 1:
            # mypy bug: https://github.com/python/mypy/issues/5485
            data.extend(filter(ep.filter, response_json))  # type: ignore
            # print(json.dumps(response_json, indent=4))
            # print(f"got {len(response_json)} elems")
            page += 1
        else:
            break

    # print(f"GOT JSON for {ep_name}")
    # print(json.dumps(data, indent=4))
    # print(f"done fetching {ep_name}")
    put_json(first_file(ep), data)

    return len(data), messages


def file_to_file_filter(
    in_files: List[str],
    out_file: str,
    # fun: Callable[[Any], TransformResult],  # FIXME: how to write this type sig ?
    fun: Callable,  # FIXME: how to write this type sig ?
) -> List[Msg]:
    data_sets = []
    for fname in in_files:
        data_sets.append(get_json(fname))

    data, messages = fun(*data_sets)
    put_json(out_file, data)
    return messages


def first_file(ep: Endpoint) -> str:
    return f"{ep.version}_{ep.name}.json"


def processed_file(ep: Endpoint, suffix: str) -> str:
    return f"FINAL_{ep.name}{suffix}.json"


# def csv_file(endpoint, suffix):
#     return f"FINAL_{endpoint['name']}{suffix}.csv"


def do_transforms(endpoints: List[Endpoint]) -> List[Msg]:
    """
    returns messages
    """
    messages = []
    for ep in endpoints:
        for suffix, trans_fn in ep.transform.items():
            src = first_file(ep)
            dst = processed_file(ep, suffix)

            messages += file_to_file_filter([src], dst, trans_fn)

    return messages


def get_json(filename: str) -> Any:
    with open(filename, "r") as f:
        return json.loads(f.read())


def put_json(filename: str, data: Any) -> None:
    with open(filename, "w") as f:
        f.write(json.dumps(data, indent=4))


SUBSCRIPTIONS = Endpoint(
    name="subscriptions",
    version="v1",
)
MEMBERSHIPS_LIFETIME = Endpoint(
    name="memberships_lifetime",
    version="v3",
    mk_url=lambda self, base_url, page: f"{base_url}v3/memberships/members?plan=sustinator-dor-pe-viata&page={page}",
)
MEMBERSHIPS_OLD = Endpoint(
    name="memberships_old",
    version="v3",
    mk_url=lambda self, base_url, page: f"{base_url}v3/memberships/members?plan=sustinatori-dor&page={page}",
    filter=lambda entry: entry.get("subscription_id") is None,
)
ORDERS = Endpoint(
    name="orders",
    version="v3",
    transform={
        "_verbose": lambda x: transform_orders(x, distribute=True),
        "_compact": lambda x: transform_orders(x, distribute=False),
    },
)
CUSTOMERS = Endpoint(
    name="customers",
    version="v3",
    transform={"": transform_customers},
    mk_url=lambda self, base_url, page: f"{base_url}v3/customers/?role=all&page={page}",
)
ENDPOINTS = [ORDERS, CUSTOMERS, SUBSCRIPTIONS, MEMBERSHIPS_OLD, MEMBERSHIPS_LIFETIME]


def main(KEY: str, SECRET: str, BASE_URL: str) -> tuple:
    fetcher = Fetcher(KEY, SECRET)

    success, messages = fetch_all(ENDPOINTS, fetcher, BASE_URL)
    messages += do_transforms(ENDPOINTS)

    # abonamente is tricky; fetching is split to allow incremental changes

    # 2nd stage fetch
    notes_fname = "v3_subscription_notes.json"
    customers_fname = "customers_index.json"
    customers_emails_fname = "customers_email_index.json"

    messages += fetch_convoluted_data_stage_2(
        fetcher,
        BASE_URL,
        SUBSCRIPTIONS,
        notes_fname,
        customers_emails_fname,
    )

    # 3rd stage fetch
    customers_data = get_json(first_file(CUSTOMERS))
    known_customers = {str(c["id"]): c for c in customers_data}

    messages += fetch_convoluted_data_stage_3(
        fetcher,
        BASE_URL,
        SUBSCRIPTIONS,
        MEMBERSHIPS_LIFETIME,
        MEMBERSHIPS_OLD,
        customers_emails_fname,
        known_customers,
        customers_fname,
    )

    # actual transformation
    dest_fname = "FINAL_abonamente.json"
    messages += file_to_file_filter(
        in_files=[
            first_file(SUBSCRIPTIONS),
            first_file(MEMBERSHIPS_LIFETIME),
            first_file(MEMBERSHIPS_OLD),
            notes_fname,
            customers_fname,
            customers_emails_fname,
        ],
        out_file=dest_fname,
        fun=transform_convoluted,
    )

    table_locations = [
        dest_fname,
        processed_file(CUSTOMERS, suffix=""),
        *(processed_file(ORDERS, suff) for suff in ORDERS.transform.keys()),
    ]

    # heuristic: if a json is under 10 bytes it can't have even one entry
    success = success and all(os.path.getsize(f) > 10 for f in table_locations)

    stats = [msg.to_str() for msg in messages]

    junk = [
        *map(first_file, ENDPOINTS),
        notes_fname,
        customers_fname,
        customers_emails_fname,
    ]
    for f in junk:
        try:
            os.remove(f)
        except FileNotFoundError:
            pass

    return (success, stats, *table_locations)


def get_or_create_table(table_fields_defs, table_name):
    db = models.Database.objects.last()
    user, _ = User.objects.get_or_create(username="paul-sync")

    table, created = models.Table.objects.get_or_create(
        name=table_name, database=db, owner=user
    )
    table.last_edit_date = timezone.now()
    table.last_edit_user = user
    table.active = True
    table.save()

    # if created:
    for field_name, field_details in table_fields_defs.items():
        column, _ = models.TableColumn.objects.get_or_create(
            table=table, name=field_name
        )
        column.display_name = field_details["display_name"]
        column.field_type = field_details["type"]
        column.save()

    return table


def run_sync(
    KEY,
    SECRET,
    ENDPOINT_URL,
    TABLE_ABONAMENTE,
    TABLE_CLIENTI,
    TABLE_COMENZI_DETALIAT,
    TABLE_COMENZI_COMPACT,
):
    """
    Do the actual sync.

    Return success (bool), updates(json), errors(json)
    """
    success = True
    map_tables = {
        "FINAL_abonamente.json": {
            "fields": SUBSCRIPTIONS_FIELDS,
            "name": TABLE_ABONAMENTE,
            "unique_field": "id_abonament",
        },
        "FINAL_customers.json": {
            "fields": CUSTOMER_FIELDS,
            "name": TABLE_CLIENTI,
            "unique_field": "id_client",
        },
        "FINAL_orders_verbose.json": {
            "fields": ORDERS_VERBOSE_FIELDS,
            "name": TABLE_COMENZI_DETALIAT,
            "unique_field": "id_produs",
        },
        "FINAL_orders_compact.json": {
            "fields": ORDERS_COMPACT_FIELDS,
            "name": TABLE_COMENZI_COMPACT,
            "unique_field": "id_comanda",
        },
    }

    try:
        # success, stats, *table_locations = (True, ['Error: GET on URL https://dor.ro/wp-json/wc/v3/customers/0 returned 404 Client Error: Not Found for url: https://www.dor.ro/wp-json/wc/v3/customers/0?consumer_key=ck_dfeab47b910ef6b5113cadc93d27b51cfff357b3&consumer_secret=cs_2a6077c83243eb84fe9b788668b29d62e9b82d40\nPlease try the action again. If the error persists contact support'], 'FINAL_abonamente.json', 'FINAL_customers.json', 'FINAL_orders_verbose.json', 'FINAL_orders_compact.json')
        # success, stats, *table_locations = (True, ['Error: GET on URL https://dor.ro/wp-json/wc/v3/customers/0 returned 404 Client Error: Not Found for url: https://www.dor.ro/wp-json/wc/v3/customers/0?consumer_key=ck_dfeab47b910ef6b5113cadc93d27b51cfff357b3&consumer_secret=cs_2a6077c83243eb84fe9b788668b29d62e9b82d40\nPlease try the action again. If the error persists contact support'], 'FINAL_abonamente.json')
        success, stats, *table_locations = main(KEY, SECRET, ENDPOINT_URL)

        for table_name in table_locations:
            print(table_name)
            table_fields_def = map_tables[table_name]["fields"]
            table = get_or_create_table(
                table_fields_def, map_tables[table_name]["name"]
            )
            json_table = json.load(open(table_name))
            i = 0
            for entry_json in json_table:
                i += 1
                unique_field = map_tables[table_name]["unique_field"]
                entry_filter = {
                    "table": table,
                    "data__{}".format(unique_field): entry_json[
                        table_fields_def[unique_field]["display_name"]
                    ],
                }
                entry = models.Entry.objects.filter(**entry_filter)
                print(table, i)

                if not entry:
                    entry = models.Entry.objects.create(
                        table=table,
                        data={
                            unique_field: entry_json[
                                table_fields_def[unique_field]["display_name"]
                            ]
                        },
                    )
                else:
                    entry = entry[0]

                entry_data = {}
                for entry_field_name in table_fields_def:
                    value = entry_json.get(
                        table_fields_def[entry_field_name]["display_name"], None
                    )
                    if table_fields_def[entry_field_name]["type"] == "enum":
                        table_column = models.TableColumn.objects.get(
                            table=table, name=entry_field_name
                        )
                        if not table_column.choices:
                            table_column.choices = []
                        if value and str(value) not in table_column.choices:
                            table_column.choices.append(value)
                            table_column.save()
                    entry_data[entry_field_name] = value

                models.Entry.objects.filter(**entry_filter).update(data=entry_data)
            # os.remove(table_name)
        stats = {"details": stats}

    except Exception as e:
        print("---Error", e)
        success = False
        stats = {"details": ["Error in utils: " + str(e)]}
    return success, stats
