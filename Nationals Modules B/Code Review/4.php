<?php

if( isset( $_POST[ 'Upload' ] ) ) {
	$target_path  = "/var/www/html/uploads/";
	$target_path .= basename( $_FILES[ 'uploaded' ][ 'name' ] );

	$uploaded_name = $_FILES[ 'uploaded' ][ 'name' ];
	$uploaded_type = $_FILES[ 'uploaded' ][ 'type' ];
	$uploaded_size = $_FILES[ 'uploaded' ][ 'size' ];

	if( ( $uploaded_type == "image/jpeg" || $uploaded_type == "image/png" ) &&
		( $uploaded_size < 100000 ) ) {

		if( !move_uploaded_file( $_FILES[ 'uploaded' ][ 'tmp_name' ], $target_path ) ) {
			$html .= '<pre>Your image was not uploaded.</pre>';
		}
		else {
			$html .= "<pre>{$target_path} succesfully uploaded!</pre>";
		}
	}
	else {
		$html .= '<pre>Your image was not uploaded. We can only accept JPEG or PNG images.</pre>';
	}
}

?>