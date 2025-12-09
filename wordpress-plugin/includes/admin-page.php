<?php
// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

function ainl_admin_page() {
    ?>
    <div class="wrap ainl-admin-wrap">
        <h1><?php echo esc_html(get_admin_page_title()); ?></h1>
        
        <div id="ainl-tabs" class="nav-tab-wrapper">
            <a href="#research-tab" class="nav-tab nav-tab-active">Research Topic</a>
            <a href="#minutes-tab" class="nav-tab">Meeting Minutes</a>
            <a href="#hybrid-tab" class="nav-tab">Combined</a>
        </div>
        
        <div id="research-tab" class="ainl-tab-content" style="display: block;">
            <h2>Generate from Research</h2>
            <form id="ainl-research-form">
                <?php wp_nonce_field('ainl_nonce', 'nonce'); ?>
                
                <table class="form-table">
                    <tr>
                        <th scope="row">
                            <label for="topic">Topic *</label>
                        </th>
                        <td>
                            <input type="text" id="topic" name="topic" class="regular-text" required />
                            <p class="description">What should the newsletter cover?</p>
                        </td>
                    </tr>
                    <tr>
                        <th scope="row">
                            <label for="context">Additional Context</label>
                        </th>
                        <td>
                            <textarea id="context" name="context" rows="5" class="large-text"></textarea>
                            <p class="description">Optional: Provide specific context or direction</p>
                        </td>
                    </tr>
                    <tr>
                        <th scope="row">
                            <label for="word_count">Target Word Count</label>
                        </th>
                        <td>
                            <input type="number" id="word_count" name="word_count" value="800" min="400" max="2000" step="100" />
                            <p class="description">Recommended: 600-1200 words</p>
                        </td>
                    </tr>
                </table>
                
                <p class="submit">
                    <button type="submit" class="button button-primary">Generate Newsletter</button>
                </p>
            </form>
        </div>
        
        <div id="minutes-tab" class="ainl-tab-content" style="display: none;">
            <h2>Generate from Meeting Minutes</h2>
            <form id="ainl-minutes-form" enctype="multipart/form-data">
                <?php wp_nonce_field('ainl_nonce', 'nonce'); ?>
                
                <table class="form-table">
                    <tr>
                        <th scope="row">
                            <label for="file">Upload Minutes *</label>
                        </th>
                        <td>
                            <input type="file" id="file" name="file" accept=".pdf,.doc,.docx,.txt" required />
                            <p class="description">Accepted: PDF, Word, Text</p>
                        </td>
                    </tr>
                    <tr>
                        <th scope="row">
                            <label for="additional_context">Additional Context</label>
                        </th>
                        <td>
                            <textarea id="additional_context" name="additional_context" rows="5" class="large-text"></textarea>
                        </td>
                    </tr>
                </table>
                
                <p class="submit">
                    <button type="submit" class="button button-primary">Generate Newsletter</button>
                </p>
            </form>
        </div>
        
        <div id="hybrid-tab" class="ainl-tab-content" style="display: none;">
            <h2>Generate Combined Newsletter</h2>
            <form id="ainl-hybrid-form" enctype="multipart/form-data">
                <?php wp_nonce_field('ainl_nonce', 'nonce'); ?>
                
                <table class="form-table">
                    <tr>
                        <th scope="row">
                            <label for="hybrid-file">Upload Minutes *</label>
                        </th>
                        <td>
                            <input type="file" id="hybrid-file" name="file" accept=".pdf,.doc,.docx,.txt" required />
                        </td>
                    </tr>
                    <tr>
                        <th scope="row">
                            <label for="research_topic">Research Topic *</label>
                        </th>
                        <td>
                            <input type="text" id="research_topic" name="research_topic" class="regular-text" required />
                        </td>
                    </tr>
                    <tr>
                        <th scope="row">
                            <label for="research_context">Research Context</label>
                        </th>
                        <td>
                            <textarea id="research_context" name="research_context" rows="3" class="large-text"></textarea>
                        </td>
                    </tr>
                </table>
                
                <p class="submit">
                    <button type="submit" class="button button-primary">Generate Combined Newsletter</button>
                </p>
            </form>
        </div>
        
        <div id="ainl-status" style="display: none;">
            <div class="ainl-spinner"></div>
            <h3>Generating newsletter...</h3>
            <p>This may take 30-60 seconds</p>
        </div>
        
        <div id="ainl-result" style="display: none;">
            <div class="notice notice-success">
                <p><strong>Newsletter Generated Successfully!</strong></p>
            </div>
            <p>
                <a href="#" id="ainl-edit-link" class="button button-primary" target="_blank">Edit in WordPress</a>
                <a href="#" id="ainl-preview-link" class="button" target="_blank">Preview</a>
            </p>
        </div>
    </div>
    <?php
}