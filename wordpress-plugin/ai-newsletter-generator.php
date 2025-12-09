<?php
/**
 * Plugin Name: AI Newsletter Generator
 * Plugin URI: https://github.com/your-repo
 * Description: Generate newsletters using AI directly from WordPress admin
 * Version: 1.0.0
 * Author: Your Name
 * License: GPL v2 or later
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

// Define plugin constants
define('AINL_VERSION', '1.0.0');
define('AINL_PLUGIN_DIR', plugin_dir_path(__FILE__));
define('AINL_PLUGIN_URL', plugin_dir_url(__FILE__));

// Include admin page
require_once AINL_PLUGIN_DIR . 'includes/admin-page.php';

// Add admin menu
add_action('admin_menu', 'ainl_add_admin_menu');

function ainl_add_admin_menu() {
    add_menu_page(
        'AI Newsletter Generator',
        'AI Newsletter',
        'edit_posts',
        'ai-newsletter-generator',
        'ainl_admin_page',
        'dashicons-email-alt',
        30
    );
}

// Enqueue admin scripts
add_action('admin_enqueue_scripts', 'ainl_enqueue_admin_scripts');

function ainl_enqueue_admin_scripts($hook) {
    if ($hook !== 'toplevel_page_ai-newsletter-generator') {
        return;
    }
    
    wp_enqueue_style(
        'ainl-admin-style',
        AINL_PLUGIN_URL . 'assets/css/admin-style.css',
        array(),
        AINL_VERSION
    );
    
    wp_enqueue_script(
        'ainl-admin-script',
        AINL_PLUGIN_URL . 'assets/js/admin-script.js',
        array('jquery'),
        AINL_VERSION,
        true
    );
    
    wp_localize_script('ainl-admin-script', 'ainlSettings', array(
        'ajaxurl' => admin_url('admin-ajax.php'),
        'nonce' => wp_create_nonce('ainl_nonce'),
        'apiUrl' => get_option('ainl_api_url', '')
    ));
}

// AJAX handler for newsletter generation
add_action('wp_ajax_ainl_generate_newsletter', 'ainl_handle_generate_newsletter');

function ainl_handle_generate_newsletter() {
    check_ajax_referer('ainl_nonce', 'nonce');
    
    if (!current_user_can('edit_posts')) {
        wp_send_json_error('Insufficient permissions');
        return;
    }
    
    $type = isset($_POST['type']) ? sanitize_text_field($_POST['type']) : '';
    $api_url = get_option('ainl_api_url', '');
    
    if (empty($api_url)) {
        wp_send_json_error('API URL not configured');
        return;
    }
    
    // Forward request to backend API
    $endpoint = $api_url . '/api/newsletter/generate/' . $type;
    
    $response = wp_remote_post($endpoint, array(
        'body' => $_POST,
        'timeout' => 120
    ));
    
    if (is_wp_error($response)) {
        wp_send_json_error($response->get_error_message());
        return;
    }
    
    $body = wp_remote_retrieve_body($response);
    $data = json_decode($body, true);
    
    wp_send_json_success($data);
}

// Add settings page
add_action('admin_menu', 'ainl_add_settings_page');

function ainl_add_settings_page() {
    add_submenu_page(
        'ai-newsletter-generator',
        'Settings',
        'Settings',
        'manage_options',
        'ai-newsletter-settings',
        'ainl_settings_page'
    );
}

function ainl_settings_page() {
    ?>
    <div class="wrap">
        <h1>AI Newsletter Generator Settings</h1>
        <form method="post" action="options.php">
            <?php
            settings_fields('ainl_settings');
            do_settings_sections('ainl_settings');
            submit_button();
            ?>
        </form>
    </div>
    <?php
}

// Register settings
add_action('admin_init', 'ainl_register_settings');

function ainl_register_settings() {
    register_setting('ainl_settings', 'ainl_api_url');
    
    add_settings_section(
        'ainl_main_section',
        'API Configuration',
        'ainl_main_section_callback',
        'ainl_settings'
    );
    
    add_settings_field(
        'ainl_api_url',
        'API URL',
        'ainl_api_url_callback',
        'ainl_settings',
        'ainl_main_section'
    );
}

function ainl_main_section_callback() {
    echo '<p>Configure the connection to your AI Newsletter Generator backend.</p>';
}

function ainl_api_url_callback() {
    $value = get_option('ainl_api_url', '');
    echo '<input type="url" name="ainl_api_url" value="' . esc_attr($value) . '" class="regular-text" />';
    echo '<p class="description">Example: https://your-backend.railway.app</p>';
}