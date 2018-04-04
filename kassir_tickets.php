<?php
class Update_Tickets{
	var $key = "****";//key
	//Указывает ID своей организаци для выбора
	var $def_venue = 449;
	//Указывает ID полей для обновления данных по выбору
	var $field_tickets_id = 506;
	var $field_abon_id = 507;
	var $alltickets = array();
	
	function __construct() {
		$this->alltickets = $this->get_kassir_tickets($this->def_venue);
		$this->update($this->field_tickets_id);
		$this->update($this->field_abon_id);
	}
	/*
	*  get_kassir_tickets
	*
	*  This function will return an array of data from XML feed of spb.kassir.ru
	*
	*  @type	function
	*  @date	03/04/2018
	*  @since	1.0.1
	*
	*  @param	null
	*  @return	(array)
	*/
	function get_kassir_tickets($venue){
		$xml_feed = file_get_contents("https://spb.kassir.ru/frame/feed/xml?key=".$this->key);
		$xml_feed = simplexml_load_string($xml_feed);
		$res_items = array();
		$res_actions = array();
		foreach($xml_feed->venues->item as $item){
			
		}
		foreach($xml_feed->events->item as $item){
			if((int)$item->venue==$venue){
				$res_items[(int)$item->id]=(string)$item->name;
				$res_actions[(int)$item->action]=(int)$item->action;
			}
		};
		$res_abons = array();
		foreach($xml_feed->actions->item as $item){
			if(in_array($item->id,$res_actions)){
				$res_abons[(int)$item->id]=(string)$item->name;
			}
		}
		return array($this->field_tickets_id=>$res_items,$this->field_abon_id=>$res_abons);
	}
	function update($post_id){
		require_once(dirname(__FILE__).'/../wp-load.php' );
		// get post
		$post = get_post( $post_id );
	
		// bail early if no post, or is not a field
		if( empty($post) || $post->post_type != 'acf-field' ) return false;
		
		$field = maybe_unserialize( $post->post_content );
		$field['choices'] = $this->alltickets[$post_id];
		$data = maybe_serialize( $field );
		$save = array(
			'ID'			=> $post->ID,
			'post_content'	=> $data,
		);
		wp_update_post( $save );
	}
}
?>
