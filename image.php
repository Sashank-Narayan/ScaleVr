<?php
	
	// open this directory 
	$myDirectory = opendir("database/");

	// get each entry
	while($entryName = readdir($myDirectory)) {
		$dirArray[] = $entryName;
	}

	// close directory
	closedir($myDirectory);

	//	count elements in array
    $indexCount	= count($dirArray);
    

    // loop through the array of files and print them all in a list
		for($index=0; $index < $indexCount; $index++) {
			$extension = substr($dirArray[$index], -3);
			if ( $extension =='jfif' or $extension =='jpg'){ // list only jpgs
				echo '
  
			<a target="_blank" href="DisplayProduct.html?database/' . $dirArray[$index] . '">
               
			  <img id="image" style="border: 1px solid #ddd; border-radius: 4px; padding: 5px;width: 150px;height:150px;"  src="database/' . $dirArray[$index] . '" alt="Image" />
			 </a>
			 
			  ';
			 
              
			}	
		}

	?>