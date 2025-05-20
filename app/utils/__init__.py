# Authentication and Security Utilities
from app.utils.jwt import (
    create_access_token,
    create_refresh_token,
    verify_token,
    get_current_user,
    refresh_access_token
)

# Geographical Utilities
from app.utils.geo_utils import (
    calculate_distance,
    address_to_coords,
    coords_to_address,
    get_route
)

# Routing and Optimization Utilities
from app.utils.routing import (
    a_star_algorithm,
    knapsack_capacity,
    combine_orders,
    calculate_route_matrix
)

# Logging Utilities
from app.utils.logger import (
    get_logger,
    log_info,
    log_warning,
    log_error,
    log_critical,
    log_debug
)

# Configuration Utilities
from app.utils.config_loader import (
    get_config,
    load_database_config,
    load_google_maps_config,
    load_logging_config,
    load_jwt_config,
    load_notification_config
)

# File Handling Utilities
from app.utils.file_handler import (
    save_uploaded_file,
    delete_file,
    move_file,
    list_files
)

# Notification Management Utilities
from app.utils.notification import (
    send_notification,
    get_unread_notifications,
    mark_notification_as_read,
    mark_all_as_read,
    delete_notification,
    get_all_notifications
)

# Common Utilities
from app.utils.common import (
    generate_uuid,
    current_timestamp,
    hash_password,
    verify_password,
    generate_checksum,
    generate_filename,
    is_valid_uuid,
    dict_to_camel_case
)

# PDF Generation Utilities
from app.utils.pdf_generator import (
    generate_order_report,
    generate_mission_report,
    generate_audit_log_report
)

# Permission Checking Utilities
from app.utils.permission_checker import (
    is_admin,
    is_moderator,
    is_driver,
    is_customer,
    require_admin,
    require_moderator,
    require_driver,
    require_customer,
    has_permission,
    check_permission
)

__all__ = [
    # JWT Utilities
    "create_access_token",
    "create_refresh_token",
    "verify_token",
    "get_current_user",
    "refresh_access_token",

    # Geo Utilities
    "calculate_distance",
    "address_to_coords",
    "coords_to_address",
    "get_route",

    # Routing Utilities
    "a_star_algorithm",
    "knapsack_capacity",
    "combine_orders",
    "calculate_route_matrix",

    # Logging Utilities
    "get_logger",
    "log_info",
    "log_warning",
    "log_error",
    "log_critical",
    "log_debug",

    # Configuration Utilities
    "get_config",
    "load_database_config",
    "load_google_maps_config",
    "load_logging_config",
    "load_jwt_config",
    "load_notification_config",

    # File Handling Utilities
    "save_uploaded_file",
    "delete_file",
    "move_file",
    "list_files",

    # Notification Utilities
    "send_notification",
    "get_unread_notifications",
    "mark_notification_as_read",
    "mark_all_as_read",
    "delete_notification",
    "get_all_notifications",

    # Common Utilities
    "generate_uuid",
    "current_timestamp",
    "hash_password",
    "verify_password",
    "generate_checksum",
    "generate_filename",
    "is_valid_uuid",
    "dict_to_camel_case",

    # PDF Generation Utilities
    "generate_order_report",
    "generate_mission_report",
    "generate_audit_log_report",

    # Permission Checking Utilities
    "is_admin",
    "is_moderator",
    "is_driver",
    "is_customer",
    "require_admin",
    "require_moderator",
    "require_driver",
    "require_customer",
    "has_permission",
    "check_permission"
]
