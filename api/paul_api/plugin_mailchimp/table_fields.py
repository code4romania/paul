# NOTES:
# The mailchimp_path parameter is optional
# The mailchimp_path can be at most 5 levels deep ('a', 'b', 'c', 'd', 'e')
# If mailchimp_path is missing, the path will be ('field_name', )


AUDIENCES_FIELDS = {
    'id': {
        'old_key': '',
        'display_name': 'Id',
        'type': 'text'
    },
    'web_id': {
        'old_key': '',
        'display_name': 'Web Id',
        'type': 'int'
    },
    'name': {
        'old_key': '',
        'display_name': 'Name',
        'type': 'text'
    },
    'permission_reminder': {
        'old_key': '',
        'display_name': 'Permission Reminder',
        'type': 'text'
    },
    'use_archive_bar': {
        'old_key': '',
        'display_name': 'Use Archive Bar',
        'type': 'bool'
    },
    'campaign_defaults_email': {
        'old_key': '',
        'display_name': 'Campaign Defaults (email)',
        'type': 'text',
        'mailchimp_path': ('campaign_defaults', 'from_email'),
    },
    'campaign_defaults_name': {
        'old_key': '',
        'display_name': 'Campaign Defaults (name)',
        'type': 'text',
        'mailchimp_path': ('campaign_defaults', 'from_name'),
    },
    'campaign_defaults_subject': {
        'old_key': '',
        'display_name': 'Campaign Defaults (subject)',
        'type': 'text',
        'mailchimp_path': ('campaign_defaults', 'subject'),
    },
    'notify_on_subscribe': {
        'old_key': '',
        'display_name': 'Notify On Subscribe',
        'type': 'text'
    },
    'notify_on_unsubscribe': {
        'old_key': '',
        'display_name': 'Notify On Unsubscribe',
        'type': 'text'
    },
    'date_created': {
        'old_key': '',
        'display_name': 'Date Created',
        'type': 'date'
    },
    'list_rating': {
        'old_key': '',
        'display_name': 'List Rating',
        'type': 'float'
    },
    'email_type_option': {
        'old_key': '',
        'display_name': 'Email Type Option',
        'type': 'bool'
    },
    'subscribe_url_short': {
        'old_key': '',
        'display_name': 'Subscribe Url Short',
        'type': 'text'
    },
    'subscribe_url_long': {
        'old_key': '',
        'display_name': 'Subscribe Url Long',
        'type': 'text'
    },
    'beamer_address': {
        'old_key': '',
        'display_name': 'Beamer Address',
        'type': 'text'
    },
    'visibility': {
        'old_key': '',
        'display_name': 'Visibility',
        'type': 'text'
    },
    'double_optin': {
        'old_key': '',
        'display_name': 'Double Optin',
        'type': 'bool'
    },
    'has_welcome': {
        'old_key': '',
        'display_name': 'Has Welcome',
        'type': 'bool'
    },
    'marketing_permissions': {
        'old_key': '',
        'display_name': 'Marketing Permissions',
        'type': 'bool'
    },
    # 'modules': {
    #     'old_key': '',
    #     'display_name': 'Modules',
    #     'type': ''
    # },
}


AUDIENCES_STATS_FIELDS = {
    'audience_id': {
        'old_key': '',
        'display_name': 'Audience ID',
        'mailchimp_path': ('stats', 'audience_id'),
        'type': 'text'
    },
    'audience_name': {
        'old_key': '',
        'display_name': 'Audience Name',
        'mailchimp_path': ('stats', 'audience_name'),
        'type': 'enum'
    },
    'avg_sub_rate': {
        'old_key': '',
        'display_name': 'Avg Sub Rate',
        'mailchimp_path': ('stats', 'avg_sub_rate'),
        'type': 'int'
    },
    'avg_unsub_rate': {
        'old_key': '',
        'display_name': 'Avg Unsub Rate',
        'mailchimp_path': ('stats', 'avg_unsub_rate'),
        'type': 'int'
    },
    'campaign_count': {
        'old_key': '',
        'display_name': 'Campaign Count',
        'mailchimp_path': ('stats', 'campaign_count'),
        'type': 'int'
    },
    'campaign_last_sent': {
        'old_key': '',
        'display_name': 'Campaign Last Sent',
        'mailchimp_path': ('stats', 'campaign_last_sent'),
        'type': 'date'
    },
    'cleaned_count': {
        'old_key': '',
        'display_name': 'Cleaned Count',
        'mailchimp_path': ('stats', 'cleaned_count'),
        'type': 'int'
    },
    'cleaned_count_since_send': {
        'old_key': '',
        'display_name': 'Cleaned Count Since Send',
        'mailchimp_path': ('stats', 'cleaned_count_since'),
        'type': 'int'
    },
    'click_rate': {
        'old_key': '',
        'display_name': 'Click Rate',
        'mailchimp_path': ('stats', 'click_rate'),
        'type': 'int'
    },
    'last_sub_date': {
        'old_key': '',
        'display_name': 'Last Sub Date',
        'mailchimp_path': ('stats', 'last_sub_date'),
        'type': 'date'
    },
    'last_unsub_date': {
        'old_key': '',
        'display_name': 'Last Unsub Date',
        'mailchimp_path': ('stats', 'last_unsub_date'),
        'type': 'date'
    },
    'member_count': {
        'old_key': '',
        'display_name': 'Member Count',
        'mailchimp_path': ('stats', 'member_count'),
        'type': 'int'
    },
    'member_count_since_send': {
        'old_key': '',
        'display_name': 'Member Count Since Send',
        'mailchimp_path': ('stats', 'member_count_since_send'),
        'type': 'int'
    },
    'merge_field_count': {
        'old_key': '',
        'display_name': 'Merge Field Count',
        'mailchimp_path': ('stats', 'merge_field_count'),
        'type': 'int'
    },
    'open_rate': {
        'old_key': '',
        'display_name': 'Open Rate',
        'mailchimp_path': ('stats', 'open_rate'),
        'type': 'int'
    },
    'target_sub_rate': {
        'old_key': '',
        'display_name': 'Target Sub Rate',
        'mailchimp_path': ('stats', 'target_sub_rate'),
        'type': 'int'
    },
    'unsubscribe_count': {
        'old_key': '',
        'display_name': 'Unsubscribe Count',
        'mailchimp_path': ('stats', 'ubsubscribe_count'),
        'type': 'int'
    },
    'unsubscribe_count_since_send': {
        'old_key': '',
        'display_name': 'Unsubscribe Count Since Send',
        'mailchimp_path': ('stats', 'ubsubscribe_count_since_send'),
        'type': 'int'
    }
}


AUDIENCE_SEGMENTS_FIELDS = {
    'audience_id': {
        'old_key': '',
        'display_name': 'Audience ID',
        'type': 'text'
    },
    'audience_name': {
        'old_key': '',
        'display_name': 'Audience Name',
        'type': 'enum'
    },
    'name': {
        'old_key': '',
        'display_name': 'Name',
        'type': 'text'
    },
    'id': {
        'old_key': '',
        'display_name': 'ID',
        'type': 'int'
    },
    'member_count': {
        'old_key': '',
        'display_name': 'Member Count',
        'type': 'int'
    },
    'type': {
        'old_key': '',
        'display_name': 'Type',
        'type': 'text'
    },
    'created_at': {
        'old_key': '',
        'display_name': 'Created At',
        'type': 'date'
    },
    'updated_at': {
        'old_key': '',
        'display_name': 'Updated At',
        'type': 'date'
    },
    'options': {
        'old_key': '',
        'display_name': 'Options',
        'type': 'text'
    }
}


MERGE_FIELDS = {
    'fname': {   # was "first_name"
        'old_key': 'first_name',
        'display_name': 'First Name',
        'type': 'text',
        'mailchimp_path': ('merge_fields', 'FNAME'),
    },
    'lname': {  # was "last_name"
        'old_key': 'last_name',
        'display_name': 'Last Name',
        'type': 'text',
        'mailchimp_path': ('merge_fields', 'LNAME'),
    },
    'phone': {
        'old_key': 'telephone',
        'display_name': 'Telephone',
        'type': 'text',
        'mailchimp_path': ('merge_fields', 'PHONE'),
    },
    'addr1': {
        'old_key': '',
        'display_name': 'Address Line 1',
        'type': 'text',
        'mailchimp_path': ('merge_fields', 'ADDRESS', 'addr1'),
    },
    'addr2': {
        'old_key': '',
        'display_name': 'Address Line 2',
        'type': 'text',
        'mailchimp_path': ('merge_fields', 'ADDRESS', 'addr2'),
    },
    'city': {
        'old_key': '',
        'display_name': 'Address City',
        'type': 'text',
        'mailchimp_path': ('merge_fields', 'ADDRESS', 'city'),
    },
    'state': {
        'old_key': '',
        'display_name': 'Address State',
        'type': 'text',
        'mailchimp_path': ('merge_fields', 'ADDRESS', 'state'),
    },
    'zip': {
        'old_key': '',
        'display_name': 'Address ZIP',
        'type': 'text',
        'mailchimp_path': ('merge_fields', 'ADDRESS', 'zip'),
    },
    'country': {
        'old_key': '',
        'display_name': 'Address Country',
        'type': 'text',
        'mailchimp_path': ('merge_fields', 'ADDRESS', 'country'),
    },
    'birthday': {
        'old_key': 'birthdate',
        'display_name': 'Birthday',
        'type': 'text',  # MM/DD or MM/DD set in Mailchimp
        'mailchimp_path': ('merge_fields', 'BIRTHDAY'),
    },
    'project': {
        'old_key': '',
        'display_name': 'Project',
        'type': 'text',
        'mailchimp_path': ('merge_fields', 'PROJECT'),
    },
    'gdpr': {
        'old_key': '',
        'display_name': 'GDPR',
        'type': 'date',
        'mailchimp_path': ('merge_fields', 'GDPR'),
    },
    # 'gdpr_permission': {
    #     'old_key': '',
    #     'display_name': 'GDPR Permission',
    #     'type': 'text'
    # },
    'contact_added_on': {
        'old_key': '',
        'display_name': 'Contact Added On',
        'type': 'date',
        'mailchimp_path': ('merge_fields', 'C_ADDEDON'),
    },
    'contact_source': {
        'old_key': '',
        'display_name': 'Contact Source',
        'type': 'text',
        'mailchimp_path': ('merge_fields', 'C_SOURCE'),
    },
}


AUDIENCE_MEMBERS_FIELDS = {
    'audience_id': {
        'old_key': '',
        'display_name': 'Audience ID',
        'type': 'text'
    },
    'audience_name': {
        'old_key': '',
        'display_name': 'Audience Name',
        'type': 'enum'
    },
    'id': {
        'old_key': '',
        'display_name': 'ID',
        'type': 'text'
    },
    'email_address': {
        'old_key': '',
        'display_name': 'Email Address',
        'type': 'text'
    },
    'unique_email_id': {
        'old_key': '',
        'display_name': 'Unique Email ID',
        'type': 'text'
    },
    # 'full_name': {  # new
    #     'old_key': '',
    #     'display_name': 'Full Name',
    #     'type': 'text'
    # },
    'web_id': {
        'old_key': '',
        'display_name': 'Web ID',
        'type': 'int'
    },
    'email_type': {
        'old_key': '',
        'display_name': 'Email Type',
        'type': 'enum'
    },
    'status': {
        'old_key': '',
        'display_name': 'Status',
        'type': 'enum'
    },
    'unsubscribe_reason': {  # new
        'old_key': '',
        'display_name': 'Unsubscribe Reason',
        'type': 'text'
    },
    'consents_to_one_to_one_messaging': {  # new
        'old_key': '',
        'display_name': 'One to One',
        'type': 'bool'
    },
    # 'merge_fields': {  # The merge_fields will contain all custom contact fields
    #     'old_key': '',
    #     'display_name': 'Merge Fields',
    #     'type': 'text'
    # },
    'interests': {  # new
        'old_key': '',
        'display_name': 'Interests',
        'type': 'text'
    },
    'avg_open_rate': {
        'old_key': '',
        'display_name': 'Stats Open',
        'type': 'int',
        'mailchimp_path': ('stats', 'avg_open_rate'),
    },
    'avg_click_rate': {
        'old_key': '',
        'display_name': 'Stats Click',
        'type': 'int',
        'mailchimp_path': ('stats', 'avg_click_rate'),
    },
    'total_revenue': {  # new
        'old_key': '',
        'display_name': 'Stats Total Revenue',
        'type': 'float',
        'mailchimp_path': ('stats', 'ecommerce_data', 'total_revenue'),
    },
    'total_orders': {  # new
        'old_key': '',
        'display_name': 'Stats Total Orders',
        'type': 'int',
        'mailchimp_path': ('stats', 'ecommerce_data', 'number_of_orders'),
    },
    'currency_code': {  # new
        'old_key': '',
        'display_name': 'Stats Currency Code',
        'type': 'text',
        'mailchimp_path': ('stats', 'ecommerce_data', 'currency_code'),
    },
    'ip_signup': {
        'old_key': '',
        'display_name': 'Signup IP',
        'type': 'text'
    },
    'timestamp_signup': {
        'old_key': '',
        'display_name': 'Signup Timestamp',
        'type': 'date'
    },
    'ip_opt': {
        'old_key': '',
        'display_name': 'Opt IP',
        'type': 'text'
    },
    'timestamp_opt': {
        'old_key': '',
        'display_name': 'Opt Timestamp',
        'type': 'date'
    },
    'member_rating': {
        'old_key': '',
        'display_name': 'Member Rating',
        'type': 'int'
    },
    'last_changed': {
        'old_key': '',
        'display_name': 'Last Changed',
        'type': 'date'
    },
    'language': {
        'old_key': '',
        'display_name': 'Language',
        'type': 'enum'
    },
    'vip': {
        'old_key': '',
        'display_name': 'VIP',
        'type': 'bool'
    },
    'email_client': {
        'old_key': '',
        'display_name': 'Email Client',
        'type': 'text'
    },
    'location_country': {
        'old_key': '',
        'display_name': 'Location Country',
        'type': 'text',
        'mailchimp_path': ('location', 'country_code'),
    },
    'location_region': {  # new
        'old_key': '',
        'display_name': 'Location Region',
        'type': 'text',
        'mailchimp_path': ('location', 'region'),
    },

    #
    # TODO: marketing_permissions
    'marketing_permissions': {  # new  # TODO: Fix it
        'old_key': '',
        'display_name': 'Marketing Permissions',
        'type': 'text',
    },
    # "marketing_permissions": [
    #   {
    #     "marketing_permission_id": "string",
    #     "text": "string",
    #     "enabled": true
    #   }
    # ],

    'last_note': {  # new
        'old_key': '',
        'display_name': 'Last Note',
        'type': 'text',
        'mailchimp_path': ('last_note', 'note'),
    },
    'source': {
        'old_key': '',
        'display_name': 'Source',
        'type': 'enum'
    },
    'tags_count': {
        'old_key': '',
        'display_name': 'Tags Count',
        'type': 'int'
    },
    'tags': {
        'old_key': '',
        'display_name': 'Tags',
        'type': 'enum',
        'is_list': True
    },
}


SEGMENT_MEMBERS_FIELDS = {
    'audience_id': {
        'old_key': '',
        'display_name': 'Audience ID',
        'type': 'text'
    },
    'audience_name': {
        'old_key': '',
        'display_name': 'Audience Name',
        'type': 'enum'
    },
    'segment_id': {
        'old_key': '',
        'display_name': 'Segment ID',
        'type': 'text'
    },
    'segment_name': {
        'old_key': '',
        'display_name': 'Segment Name',
        'type': 'text'
    },
    'id': {
        'old_key': '',
        'display_name': 'ID',
        'type': 'text'
    },
    'email_address': {
        'old_key': '',
        'display_name': 'Email Address',
        'type': 'text'
    },
    'unique_email_id': {
        'old_key': '',
        'display_name': 'Unique Email Id',
        'type': 'text'
    },
    'email_type': {
        'old_key': '',
        'display_name': 'Email Type',
        'type': 'enum'
    },
    'status': {
        'old_key': '',
        'display_name': 'Status',
        'type': 'enum'
    },
    'stats_click': {
        'old_key': '',
        'display_name': 'Stats Click',
        'type': 'int',
        'mailchimp_path': ('stats', 'avg_click_rate'),
    },
    'stats_open': {
        'old_key': '',
        'display_name': 'Stats Open',
        'type': 'int',
        'mailchimp_path': ('stats', 'avg_open_rate'),
    },
    'ip_signup': {
        'old_key': '',
        'display_name': 'Ip Signup',
        'type': 'text'
    },
    'timestamp_signup': {
        'old_key': '',
        'display_name': 'Timestamp Signup',
        'type': 'date'
    },
    'ip_opt': {
        'old_key': '',
        'display_name': 'Ip Opt',
        'type': 'text'
    },
    'timestamp_opt': {
        'old_key': '',
        'display_name': 'Timestamp Opt',
        'type': 'date'
    },
    'member_rating': {
        'old_key': '',
        'display_name': 'Member Rating',
        'type': 'int'
    },
    'last_changed': {
        'old_key': '',
        'display_name': 'Last Changed',
        'type': 'date'
    },
    'language': {
        'old_key': '',
        'display_name': 'Language',
        'type': 'enum'
    },
    'vip': {
        'old_key': '',
        'display_name': 'Vip',
        'type': 'bool'
    },
    'email_client': {
        'old_key': '',
        'display_name': 'Email Client',
        'type': 'text'
    },
    'location_country': {
        'old_key': '',
        'display_name': 'Location Country',
        'type': 'text',
        'mailchimp_path': ('location', 'country_code'),
    }
}

AUDIENCE_TAGS_FIELDS = {
    'id': {
        'old_key': '',
        'display_name': 'ID',
        'type': 'text'
    },
    'name': {
        'old_key': '',
        'display_name': 'Name',
        'type': 'enum'
    },
    'audience_id': {
        'old_key': '',
        'display_name': 'Audience ID',
        'type': 'text'
    },
    'audience_name': {
        'old_key': '',
        'display_name': 'Audience Name',
        'type': 'text'
    },
}


TABLE_MAPPING = {
    'audiences': AUDIENCES_FIELDS,
    'audiences_stats': AUDIENCES_STATS_FIELDS,
    'audience_segments': AUDIENCE_SEGMENTS_FIELDS,
    'contact_merge_fields': MERGE_FIELDS,
    'audience_members': AUDIENCE_MEMBERS_FIELDS,
    'segment_members': SEGMENT_MEMBERS_FIELDS,
    'audience_tags': AUDIENCE_TAGS_FIELDS,
}
