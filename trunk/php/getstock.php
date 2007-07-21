<? 
function getSohuQuote($stockSymbol = "000001") 
{ 
if (!$targetURL) $targetURL = "http://quotes.money.163.com/quote/$stockSymbol.html"; //设定要抓取的URL目标 
$fd = fopen("$targetURL", "r"); 
$stopExtract = 0; 
$startExtract = 0; 
while (!feof($fd)) 
{ 
	$buffer = fgets($fd, 4096); 
	
	if (!$startExtract)
	{
		if (strstr($buffer, "成交")) 
		{ 
			$startExtract = 1; 
		}
	}
 
	if ($startExtract && !$stopExtract) 
	{ 
		$buffer = str_replace("</td>", "|", $buffer); 
		$buffer = str_replace("&nbsp;", "", $buffer); 
		$buffer = trim(strip_tags($buffer)); 
		if (strstr($buffer, "旧版行情系统")) 
		{ 
			$stopExtract = 1; 
		}
		$capturedHTML .= $buffer; 
	} 
	if ($startExtract && strstr($buffer, "旧版行情系统")) 
	{ 
		$stopExtract = 1;
		
		$capturedHTML = str_replace("万", "", $capturedHTML); 
		$capturedHTML = str_replace("手", "", $capturedHTML); 
		
		$parts = split("\|",$capturedHTML);
		if (count($parts)>2)
   	{
   		$capturedHTML="|";
   		if (count($parts)>36)
   		{
   			$num=36;
   		}
   		else
   		{
   			$num=count($parts);
   		}
   		for ($i=1;$i<$num;$i=$i+2) 
   		{
   				$capturedHTML=$capturedHTML.$parts[$i]."|";		
     	}
   }

		echo $capturedHTML; 
		break; 
	} 
	$lineCount++; 
} 
fclose($fd); 
} 

//以下为抓取的一个例子 
//$symbols = array('000001','000002','000003','000004' ); 
//$symbolCount = count($symbols); 
//for ($i=0; $i< $symbolCount; $i++) 
//{ 
//	getSohuQuote("$symbols[$i]");
	$code=$_GET['code'];
	getSohuQuote("$code"); 
//} 
?> 
