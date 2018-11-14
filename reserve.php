<?php

/**
 * The single template specifically designed for the shortcode.
 * This file may be overridden by copying it into your theme directory, into a folder titled
 * wpinventory/views/single-item.php While inventory does not use the WP post types, it does model functions after the
 * WP core functions to provide similar functionality.
 * */

wpinventory_get_items();
if ( wpinventory_have_items() ) {
  while ( wpinventory_have_items() ) {
    wpinventory_the_item();
    $inventory_display = wpinventory_get_display_settings( 'detail' );
    $display_labels    = wpinventory_get_config( 'display_detail_labels' );
    ?>
        <div class="<?php wpinventory_class(); ?>">
      <?php foreach ( $inventory_display AS $sort => $field ) {
        if ($field === 'inventory_status') {
          // this is what needs to change. you need to find where in the plugin wpinventory_the_label() is declared, and figure out how to just get the value of the inventory status returned. - Sam
          if ( wpinventory_the_label( $field ) !== 'Reserved') {
            // Newly-created variable to be checked later on - Sam
            $item_available = true;
          } else {
            $item_available = false;
          }
        }
        do_action( 'wpim_single_before_the_field', $field, $inventory_display );
                do_action( 'wpim_single_before_the_field_' . $field, $inventory_display ); ?>
                <div class="<?php echo $field; ?>">
          <?php if ( $display_labels ) { ?>
                        <span class="wpinventory_label"><?php wpinventory_the_label( $field ); ?></span>
          <?php }

          wpinventory_the_field( $field ); ?>
                </div>
        <?php do_action( 'wpim_the_field_' . $field, $inventory_display ); ?>
        <?php do_action( 'wpim_the_field_close', $field, $inventory_display ); ?>
      <?php } ?>
        </div>
  <?php }
  wpinventory_backlink();

  do_action( 'wpim_before_reserve_form' );
  
  // This is where we check whether or not the item is available, and conditionally render it - Sam
  if ($item_available) {

    echo $reserve_form = wpinventory_reserve_form();
    
  }

  do_action( 'wpim_after_reserve_form' );
}