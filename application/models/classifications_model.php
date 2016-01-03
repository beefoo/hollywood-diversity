<?php
class Classifications_model extends CI_Model {
  function __construct() {
    parent::__construct();
  }

  function accessibleFields(){
    return array('imdb_id', 'gender', 'races', 'reference_url', 'image_url', 'note');
  }

  function imdbIdsClassified(){
    $query = $this->db->distinct()->select('imdb_id')->get('classifications');
    $imdb_ids = array();
    foreach ($query->result() as $row) {
      array_push($imdb_ids, $row->imdb_id);
    }
    return $imdb_ids;
  }

  function imdbIdsClassifiedByUser($user_id){
    $query = $this->db->select('imdb_id')->get_where('classifications', array('user_id' => $user_id));
    $imdb_ids = array();
    foreach ($query->result() as $row) {
      array_push($imdb_ids, $row->imdb_id);
    }
    return $imdb_ids;
  }

  function getEntryById($id){
    $query = $this->db->get_where('classifications', array('id' => $id), 1);
    $result = $query->result();
    return (count($result) > 0) ? $result[0] : FALSE;
  }

  function getEntriesByUser($user_id){
    $query = $this->db->select('imdb_id')->get_where('classifications', array('user_id' => $user_id));
    return $query->result();
  }

  function insertEntry($data) {
    $data['date_created'] = time();
    $this->db->insert('classifications', $data);
  }

  function updateEntry($id, $data) {
    $data['date_modified'] = time();
    $this->db->update('classifications', $data, array('id' => $id));
  }

}
