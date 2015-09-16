<?php

defined('BASEPATH') OR exit('No direct script access allowed');

class Migration_Add_classifications extends CI_Migration {

  public function up() {

    $this->dbforge->add_field(array(
      'id' => array('type' => 'INT', 'constraint' => 5, 'unsigned' => TRUE, 'auto_increment' => TRUE),
      'user_id' => array('type' => 'VARCHAR','constraint' => 40, 'null' => FALSE),
      'imdb_id' => array('type' => 'VARCHAR','constraint' => 40, 'null' => FALSE),
      'gender' => array('type' => 'VARCHAR', 'constraint' => 20, 'null' => FALSE),
      'races' => array('type' => 'VARCHAR','constraint' => 40, 'null' => FALSE),
      'note' => array('type' => 'VARCHAR','constraint' => 1000, 'null' => FALSE),
      'date_created' => array('type' => 'INT', 'unsigned' => TRUE, 'constraint' => 10, 'null' => FALSE),
      'date_modified' => array('type' => 'INT', 'unsigned' => TRUE, 'constraint' => 10, 'null' => FALSE)
    ));

    $this->dbforge->add_key('id', TRUE);
    $this->dbforge->add_key('user_id');

    $this->dbforge->create_table('classifications');
  }

  public function down() {
    $this->dbforge->drop_table('classifications');
  }

}
