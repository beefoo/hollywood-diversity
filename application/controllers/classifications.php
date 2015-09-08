<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

class Classifications extends CI_Controller {

  public function index(){}

  public function show($id){}

  public function add(){
    $data = array(
      "title" => "Classify"
    );
    $this->load->view('layout/head', $data);
    $this->load->view('classifications/add', $data);
    $this->load->view('layout/foot', $data);
  }

  public function edit($id){}

  public function create(){}

  public function update($id){}

  public function destroy($id){}
}

/* End of file classifications.php */
/* Location: ./application/controllers/classifications.php */
