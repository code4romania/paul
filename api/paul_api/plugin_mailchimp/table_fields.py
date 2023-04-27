
AUDIENCES_FIELDS = {
    'id': {
        'display_name': 'Id',
        'type': 'text'
    },
    'web_id': {
        'display_name': 'Web Id',
        'type': 'int'
    },
    'name': {
        'display_name': 'Name',
        'type': 'text'
    },
    'permission_reminder': {
        'display_name': 'Permission Reminder',
        'type': 'text'
    },
    'use_archive_bar': {
        'display_name': 'Use Archive Bar',
        'type': 'bool'
    },
    'campaign_defaults_email': {
        'display_name': 'Campaign Defaults (email)',
        'type': 'text',
        'mailchimp_path': ('campaign_defaults', 'from_email'),
    },
    'campaign_defaults_name': {
        'display_name': 'Campaign Defaults (name)',
        'type': 'text',
        'mailchimp_path': ('campaign_defaults', 'from_name'),
    },
    'campaign_defaults_subject': {
        'display_name': 'Campaign Defaults (subject)',
        'type': 'text',
        'mailchimp_path': ('campaign_defaults', 'subject'),
    },
    'notify_on_subscribe': {
        'display_name': 'Notify On Subscribe',
        'type': 'text'
    },
    'notify_on_unsubscribe': {
        'display_name': 'Notify On Unsubscribe',
        'type': 'text'
    },
    'date_created': {
        'display_name': 'Date Created',
        'type': 'date'
    },
    'list_rating': {
        'display_name': 'List Rating',
        'type': 'float'
    },
    'email_type_option': {
        'display_name': 'Email Type Option',
        'type': 'bool'
    },
    'subscribe_url_short': {
        'display_name': 'Subscribe Url Short',
        'type': 'text'
    },
    'subscribe_url_long': {
        'display_name': 'Subscribe Url Long',
        'type': 'text'
    },
    'beamer_address': {
        'display_name': 'Beamer Address',
        'type': 'text'
    },
    'visibility': {
        'display_name': 'Visibility',
        'type': 'text'
    },
    'double_optin': {
        'display_name': 'Double Optin',
        'type': 'bool'
    },
    'has_welcome': {
        'display_name': 'Has Welcome',
        'type': 'bool'
    },
    'marketing_permissions': {
        'display_name': 'Marketing Permissions',
        'type': 'bool'
    },
    # 'modules': {
    #     'display_name': 'Modules',
    #     'type': ''
    # },
}


AUDIENCES_STATS_FIELDS = {
    'audience_id': {
        'display_name': 'Audience ID',
        'mailchimp_path': ('stats', 'audience_id'),
        'type': 'text'
    },
    'audience_name': {
        'display_name': 'Audience Name',
        'mailchimp_path': ('stats', 'audience_name'),
        'type': 'enum'
    },
    'avg_sub_rate': {
        'display_name': 'Avg Sub Rate',
        'mailchimp_path': ('stats', 'avg_sub_rate'),
        'type': 'int'
    },
    'avg_unsub_rate': {
        'display_name': 'Avg Unsub Rate',
        'mailchimp_path': ('stats', 'avg_unsub_rate'),
        'type': 'int'
    },
    'campaign_count': {
        'display_name': 'Campaign Count',
        'mailchimp_path': ('stats', 'campaign_count'),
        'type': 'int'
    },
    'campaign_last_sent': {
        'display_name': 'Campaign Last Sent',
        'mailchimp_path': ('stats', 'campaign_last_sent'),
        'type': 'date'
    },
    'cleaned_count': {
        'display_name': 'Cleaned Count',
        'mailchimp_path': ('stats', 'cleaned_count'),
        'type': 'int'
    },
    'cleaned_count_since_send': {
        'display_name': 'Cleaned Count Since Send',
        'mailchimp_path': ('stats', 'cleaned_count_since'),
        'type': 'int'
    },
    'click_rate': {
        'display_name': 'Click Rate',
        'mailchimp_path': ('stats', 'click_rate'),
        'type': 'int'
    },
    'last_sub_date': {
        'display_name': 'Last Sub Date',
        'mailchimp_path': ('stats', 'last_sub_date'),
        'type': 'date'
    },
    'last_unsub_date': {
        'display_name': 'Last Unsub Date',
        'mailchimp_path': ('stats', 'last_unsub_date'),
        'type': 'date'
    },
    'member_count': {
        'display_name': 'Member Count',
        'mailchimp_path': ('stats', 'member_count'),
        'type': 'int'
    },
    'member_count_since_send': {
        'display_name': 'Member Count Since Send',
        'mailchimp_path': ('stats', 'member_count_since_send'),
        'type': 'int'
    },
    'merge_field_count': {
        'display_name': 'Merge Field Count',
        'mailchimp_path': ('stats', 'merge_field_count'),
        'type': 'int'
    },
    'open_rate': {
        'display_name': 'Open Rate',
        'mailchimp_path': ('stats', 'open_rate'),
        'type': 'int'
    },
    'target_sub_rate': {
        'display_name': 'Target Sub Rate',
        'mailchimp_path': ('stats', 'target_sub_rate'),
        'type': 'int'
    },
    'unsubscribe_count': {
        'display_name': 'Unsubscribe Count',
        'mailchimp_path': ('stats', 'ubsubscribe_count'),
        'type': 'int'
    },
    'unsubscribe_count_since_send': {
        'display_name': 'Unsubscribe Count Since Send',
        'mailchimp_path': ('stats', 'ubsubscribe_count_since_send'),
        'type': 'int'
    }
}


AUDIENCE_SEGMENTS_FIELDS = {
    'audience_id': {
        'display_name': 'Audience ID',
        'type': 'text'
    },
    'audience_name': {
        'display_name': 'Audience Name',
        'type': 'enum'
    },
    'name': {
        'display_name': 'Name',
        'type': 'text'
    },
    'id': {
        'display_name': 'ID',
        'type': 'int'
    },
    'member_count': {
        'display_name': 'Member Count',
        'type': 'int'
    },
    'type': {
        'display_name': 'Type',
        'type': 'text'
    },
    'created_at': {
        'display_name': 'Created At',
        'type': 'date'
    },
    'updated_at': {
        'display_name': 'Updated At',
        'type': 'date'
    },
    'options': {
        'display_name': 'Options',
        'type': 'text'
    }
}


CONTACT_FIELDS = {
    'fname': {   # was "first_name"
        'display_name': 'First Name',
        'type': 'text',
        'mailchimp_path': ('merge_fields', 'FNAME'),
    },
    'lname': {  # was "last_name"
        'display_name': 'Last Name',
        'type': 'text',
        'mailchimp_path': ('merge_fields', 'LNAME'),
    },
    # # This field is in AUDIENCE_MEMBERS_FIELDS
    # 'email_address': {
    #     'display_name': 'Email Address',
    #     'type': 'text'
    # },
    'phone': {  # was "phone"
        'display_name': 'Telephone',
        'type': 'text',
        'mailchimp_path': ('merge_fields', 'PHONE'),
    },
    'city': {
        'display_name': 'City',
        'type': 'text'
    },
    'birthday': {  # was "birthdate"
        'display_name': 'Birthday',
        'type': 'text',  # MM/DD or MM/DD set in Mailchimp
        'mailchimp_path': ('merge_fields', 'BIRTHDAY'),
    },
    'project': {
        'display_name': 'Project',
        'type': 'text',
        'mailchimp_path': ('merge_fields', 'PROJECT'),
    },
    'gdpr': {
        'display_name': 'GDPR',
        'type': 'date',
        'mailchimp_path': ('merge_fields', 'GDPR'),
    },
    # 'gdpr_permission': {
    #     'display_name': 'GDPR Permission',
    #     'type': 'text'
    # },
    'contact_added_on': {
        'display_name': 'Added On',
        'type': 'date',
        'mailchimp_path': ('merge_fields', 'C_ADDEDON'),
    },
    'contact_source': {
        'display_name': 'Source',
        'type': 'text',
        'mailchimp_path': ('merge_fields', 'C_SOURCE'),
    },
}


AUDIENCE_MEMBERS_FIELDS = {
    'audience_id': {
        'display_name': 'Audience ID',
        'type': 'text'
    },
    'audience_name': {
        'display_name': 'Audience Name',
        'type': 'enum'
    },
    'id': {
        'display_name': 'ID',
        'type': 'text'
    },
    'email_address': {
        'display_name': 'Email Address',
        'type': 'text'
    },
    'unique_email_id': {
        'display_name': 'Unique Email Id',
        'type': 'text'
    },
    # 'full_name': {  # new
    #     'display_name': 'Full Name',
    #     'type': 'text'
    # },
    'web_id': {
        'display_name': 'Web Id',
        'type': 'int'
    },
    'email_type': {
        'display_name': 'Email Type',
        'type': 'enum'
    },
    'status': {
        'display_name': 'Status',
        'type': 'enum'
    },
    'unsubscribe_reason': {  # new
        'display_name': 'Unsubscribe Reason',
        'type': 'text'
    },
    'consents_to_one_to_one_messaging': {  # new
        'display_name': 'One to One',
        'type': 'bool'
    },
    # 'merge_fields': {  # The merge_fields will contain all custom contact fields
    #     'display_name': 'Merge Fields',
    #     'type': 'text'
    # },
    'interests': {  # new
        'display_name': 'Interests',
        'type': 'text'
    },
    'avg_open_rate': {
        'display_name': 'Stats Open',
        'type': 'int',
        'mailchimp_path': ('stats', 'avg_open_rate'),
    },
    'avg_click_rate': {
        'display_name': 'Stats Click',
        'type': 'int',
        'mailchimp_path': ('stats', 'avg_click_rate'),
    },
    'total_revenue': {  # new
        'display_name': 'Total Revenue',
        'type': 'int',
        'mailchimp_path': ('stats', 'ecommerce_data', 'total_revenue'),
    },
    'total_orders': {  # new
        'display_name': 'Total Orders',
        'type': 'int',
        'mailchimp_path': ('stats', 'ecommerce_data', 'number_of_orders'),
    },
    'total_orders': {  # new
        'display_name': 'Currency',
        'type': 'text',
        'mailchimp_path': ('stats', 'ecommerce_data', 'currency_code'),
    },
    'ip_signup': {
        'display_name': 'IP Signup',
        'type': 'text'
    },
    'timestamp_signup': {
        'display_name': 'Timestamp Signup',
        'type': 'date'
    },
    'ip_opt': {
        'display_name': 'IP Opt',
        'type': 'text'
    },
    'timestamp_opt': {
        'display_name': 'Timestamp Opt',
        'type': 'date'
    },
    'member_rating': {
        'display_name': 'Member Rating',
        'type': 'int'
    },
    'last_changed': {
        'display_name': 'Last Changed',
        'type': 'date'
    },
    'language': {
        'display_name': 'Language',
        'type': 'enum'
    },
    'vip': {
        'display_name': 'VIP',
        'type': 'bool'
    },
    'email_client': {
        'display_name': 'Email Client',
        'type': 'text'
    },
    'location_country': {
        'display_name': 'Country',
        'type': 'text',
        'mailchimp_path': ('location', 'country_code'),
    },
    'location_region': {  # new
        'display_name': 'Region',
        'type': 'text',
        'mailchimp_path': ('location', 'region'),
    },

    #
    # TODO: marketing_permissions
    'marketing_permissions': {  # new  # TODO: Fix it
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
        'display_name': 'Last Note',
        'type': 'text',
        'mailchimp_path': ('last_note', 'note'),
    },
    'source': {
        'display_name': 'Source',
        'type': 'enum'
    },
    'tags_count': {
        'display_name': 'Tags Count',
        'type': 'int'
    },
    'tags': {
        'display_name': 'Tags',
        'type': 'enum',
        'is_list': True
    },
}


SEGMENT_MEMBERS_FIELDS = {
    'audience_id': {
        'display_name': 'Audience ID',
        'type': 'text'
    },
    'audience_name': {
        'display_name': 'Audience Name',
        'type': 'enum'
    },
    'segment_id': {
        'display_name': 'Segment ID',
        'type': 'text'
    },
    'segment_name': {
        'display_name': 'Segment Name',
        'type': 'text'
    },
    'id': {
        'display_name': 'ID',
        'type': 'text'
    },
    'email_address': {
        'display_name': 'Email Address',
        'type': 'text'
    },
    'unique_email_id': {
        'display_name': 'Unique Email Id',
        'type': 'text'
    },
    'email_type': {
        'display_name': 'Email Type',
        'type': 'enum'
    },
    'status': {
        'display_name': 'Status',
        'type': 'enum'
    },
    'merge_fields': {
        'display_name': 'Merge Fields',
        'type': 'text'
    },
    'stats_click': {
        'display_name': 'Stats Click',
        'type': 'int',
        'mailchimp_path': ('stats', 'avg_click_rate'),
    },
    'stats_open': {
        'display_name': 'Stats Open',
        'type': 'int',
        'mailchimp_path': ('stats', 'avg_open_rate'),
    },
    'ip_signup': {
        'display_name': 'Ip Signup',
        'type': 'text'
    },
    'timestamp_signup': {
        'display_name': 'Timestamp Signup',
        'type': 'date'
    },
    'ip_opt': {
        'display_name': 'Ip Opt',
        'type': 'text'
    },
    'timestamp_opt': {
        'display_name': 'Timestamp Opt',
        'type': 'date'
    },
    'member_rating': {
        'display_name': 'Member Rating',
        'type': 'int'
    },
    'last_changed': {
        'display_name': 'Last Changed',
        'type': 'date'
    },
    'language': {
        'display_name': 'Language',
        'type': 'enum'
    },
    'vip': {
        'display_name': 'Vip',
        'type': 'bool'
    },
    'email_client': {
        'display_name': 'Email Client',
        'type': 'text'
    },
    'location_country': {
        'display_name': 'Location',
        'type': 'text',
        'mailchimp_path': ('location', 'country_code'),
    }
}


TABLE_MAPPING = {
    'audiences': AUDIENCES_FIELDS,
    'audiences_stats': AUDIENCES_STATS_FIELDS,
    'audience_segments': AUDIENCE_SEGMENTS_FIELDS,
    'contact_fields': CONTACT_FIELDS,
    'audience_members': AUDIENCE_MEMBERS_FIELDS,
    'segment_members': SEGMENT_MEMBERS_FIELDS,
}
