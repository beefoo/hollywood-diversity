<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

class Home extends CI_Controller {

	public function index()
	{
		$data = array(
			"title" => "Homepage"
		);
		$this->load->view('layout/head', $data);
		$this->load->view('home/index', $data);
		$this->load->view('layout/foot', $data);
	}
}

/* End of file home.php */
/* Location: ./application/controllers/home.php */
