<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

class Classifications extends CI_Controller {

  public function __construct() {
    parent::__construct();

    $this->load->model('classifications_model');
  }

  public function index(){}

  public function me(){}

  public function show($id){}

  public function add(){
    $user_id = $this->input->ip_address();
    $data = array(
      'title' => 'Classify',
      'user_id' => $user_id,
      'classifications' => $this->classifications_model->getEntriesByUser($user_id)
    );
    $this->load->view('layout/head', $data);
    $this->load->view('classifications/add', $data);
    $this->load->view('layout/foot', $data);
  }

  public function edit($id){}

  public function create(){
    $data = $this->_getData();
    $data['user_id'] = $this->input->ip_address();
    $this->classifications_model->insertEntry($data);
    echo json_encode(array('message' => 'success'));
  }

  public function update($id){}

  public function destroy($id){}

  private function _cleanInput($value){

    if (!is_numeric($value)) $value = strip_tags($value);

    return $value;
  }

  private function _getData(){
    $fields = $this->classifications_model->accessibleFields();
    $data = array();

    foreach($fields as $field){
      $data[$field] = $this->_cleanInput($this->input->get_post($field));
    }

    return $data;
  }
}

/* End of file classifications.php */
/* Location: ./application/controllers/classifications.php */
