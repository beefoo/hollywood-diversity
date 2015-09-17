<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

class Pages extends CI_Controller {

	public function guide()
	{
		$data = array(
			"title" => "Guide"
		);
		$this->load->view('layout/head', $data);
		$this->load->view('pages/guide', $data);
		$this->load->view('layout/foot', $data);
	}
}

/* End of file pages.php */
/* Location: ./application/controllers/pages.php */
