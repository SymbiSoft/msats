<? 
function getSohuQuote($stockSymbol = "000001") 
{ 
if (!$targetURL) $targetURL = "http://quotes.money.163.com/quote/$stockSymbol.html"; //�趨Ҫץȡ��URLĿ�� 
$fd = fopen("$targetURL", "r"); 
$stopExtract = 0; 
$startExtract = 0; 
while (!feof($fd)) 
{ 
	$buffer = fgets($fd, 4096); 
	
	if (!$startExtract)
	{
		if (strstr($buffer, "�ɽ�")) 
		{ 
			$startExtract = 1; 
		}
	}
 
	if ($startExtract && !$stopExtract) 
	{ 
		$buffer = str_replace("</td>", "|", $buffer); 
		$buffer = str_replace("&nbsp;", "", $buffer); 
		$buffer = trim(strip_tags($buffer)); 
		if (strstr($buffer, "�ɰ�����ϵͳ")) 
		{ 
			$stopExtract = 1; 
		}
		$capturedHTML .= $buffer; 
	} 
	if ($startExtract && strstr($buffer, "�ɰ�����ϵͳ")) 
	{ 
		$stopExtract = 1;
		
		$capturedHTML = str_replace("��", "", $capturedHTML); 
		$capturedHTML = str_replace("��", "", $capturedHTML); 
		
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

//����Ϊץȡ��һ������ 
//$symbols = array('000001','000002','000003','000004' ); 
//$symbolCount = count($symbols); 
//for ($i=0; $i< $symbolCount; $i++) 
//{ 
//	getSohuQuote("$symbols[$i]");
	$code=$_GET['code'];
	getSohuQuote("$code"); 
//} 
?> 
