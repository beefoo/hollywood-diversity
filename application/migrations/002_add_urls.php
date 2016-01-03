<?php

defined('BASEPATH') OR exit('No direct script access allowed');

class Migration_Add_urls extends CI_Migration {

  public function up() {
    $fields = array(
      'reference_url' => array('type' => 'VARCHAR', 'constraint' => 1000),
      'image_url' => array('type' => 'VARCHAR', 'constraint' => 1000)
    );
    $this->dbforge->add_column('classifications', $fields);
  }

  public function down() {
    $this->dbforge->drop_column('classifications', 'reference_url');
    $this->dbforge->drop_column('classifications', 'image_url');
  }

}
