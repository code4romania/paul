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
        'mailchimp_parent_key_name': 'campaign_defaults',
        'mailchimp_key_name': 'from_email',
    },
    'campaign_defaults_name': {
        'display_name': 'Campaign Defaults (name)',
        'type': 'text',
        'mailchimp_parent_key_name': 'campaign_defaults',
        'mailchimp_key_name': 'from_name',
    },
    'campaign_defaults_subject': {
        'display_name': 'Campaign Defaults (subject)',
        'type': 'text',
        'mailchimp_parent_key_name': 'campaign_defaults',
        'mailchimp_key_name': 'subject',
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
        'type': 'text'
    },
    'audience_name': {
        'display_name': 'Audience Name',
        'type': 'enum'
    },
    'avg_sub_rate': {
        'display_name': 'Avg Sub Rate',
        'type': 'int'
    },
    'avg_unsub_rate': {
        'display_name': 'Avg Unsub Rate',
        'type': 'int'
    },
    'campaign_count': {
        'display_name': 'Campaign Count',
        'type': 'int'
    },
    'campaign_last_sent': {
        'display_name': 'Campaign Last Sent',
        'type': 'date'
    },
    'cleaned_count': {
        'display_name': 'Cleaned Count',
        'type': 'int'
    },
    'cleaned_count_since_send': {
        'display_name': 'Cleaned Count Since Send',
        'type': 'int'
    },
    'click_rate': {
        'display_name': 'Click Rate',
        'type': 'int'
    },
    'last_sub_date': {
        'display_name': 'Last Sub Date',
        'type': 'date'
    },
    'last_unsub_date': {
        'display_name': 'Last Unsub Date',
        'type': 'date'
    },
    'member_count': {
        'display_name': 'Member Count',
        'type': 'int'
    },
    'member_count_since_send': {
        'display_name': 'Member Count Since Send',
        'type': 'int'
    },
    'merge_field_count': {
        'display_name': 'Merge Field Count',
        'type': 'int'
    },
    'open_rate': {
        'display_name': 'Open Rate',
        'type': 'int'
    },
    'target_sub_rate': {
        'display_name': 'Target Sub Rate',
        'type': 'int'
    },
    'unsubscribe_count': {
        'display_name': 'Unsubscribe Count',
        'type': 'int'
    },
    'unsubscribe_count_since_send': {
        'display_name': 'Unsubscribe Count Since Send',
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
    'merge_fields': {
        'display_name': 'Merge Fields',
        'type': 'text'
    },
    'stats_click': {
        'display_name': 'Stats Click',
        'type': 'int',
        'mailchimp_parent_key_name': 'stats',
        'mailchimp_key_name': 'avg_click_rate',
    },
    'stats_open': {
        'display_name': 'Stats Open',
        'type': 'int',
        'mailchimp_parent_key_name': 'stats',
        'mailchimp_key_name': 'avg_open_rate',
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
        'mailchimp_parent_key_name': 'location',
        'mailchimp_key_name': 'country_code',
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
        'mailchimp_parent_key_name': 'stats',
        'mailchimp_key_name': 'avg_click_rate',
    },
    'stats_open': {
        'display_name': 'Stats Open',
        'type': 'int',
        'mailchimp_parent_key_name': 'stats',
        'mailchimp_key_name': 'avg_open_rate',
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
        'mailchimp_parent_key_name': 'location',
        'mailchimp_key_name': 'country_code',
    }


}

TABLE_MAPPING = {
    'audiences': AUDIENCES_FIELDS,
    'audiences_stats': AUDIENCES_STATS_FIELDS,
    'audience_segments': AUDIENCE_SEGMENTS_FIELDS,
    'audience_members': AUDIENCE_MEMBERS_FIELDS,
    'segment_members': SEGMENT_MEMBERS_FIELDS,
}
