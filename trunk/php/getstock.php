<? 
function get163Quote($stockSymbol = "000001") 
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
   			$capturedHTML="";
   			if (count($parts)>36)
   			{
   				$capturedHTML=$capturedHTML.$parts[1]."|".$parts[9];
			
   			}
     		}

		echo $capturedHTML; 
		break; 
	} 
	$lineCount++; 
} 
fclose($fd); 
} 

function getSohuQuote($stockSymbol = "000001") 
{ 
if (!$targetURL) $targetURL = "http://stock.business.sohu.com/stock_image/realtime_table.php?code=$stockSymbol"; //设定要抓取的URL目标 
$fd = fopen("$targetURL", "r"); 
$stopExtract = 0; 
$startExtract = 0; 
while (!feof($fd)) 
{ 
	$buffer = fgets($fd, 4096); 
	
	if (!$startExtract)
	{
		if (strstr($buffer, "相关")) 
		{ 
			$startExtract = 1; 
		}
	}
 
	if ($startExtract && !$stopExtract) 
	{ 
		$buffer = str_replace("</td>", "|", $buffer); 
		$buffer = str_replace("&nbsp;", "", $buffer); 
		$buffer = trim(strip_tags($buffer)); 
		if (strstr($buffer, "Ｂ")) 
		{ 
			$stopExtract = 1; 
		} 
		$capturedHTML .= $buffer; 
	} 
	if ($startExtract && strstr($buffer, "Ｂ")) 
	{ 
		$stopExtract = 1;
		$capturedHTML = str_replace("相关", "", $capturedHTML); 
		$capturedHTML = str_replace("ＫＦＨＴＮＢ||", "", $capturedHTML); 
		$capturedHTML = str_replace("|Ｋ- Ｋ线走势图Ｆ- 重要财务指标Ｈ- 历史成交明细Ｔ- 技术指标Ｎ- 最新资讯Ｂ- 网友留言", "", $capturedHTML);  
		
		
		$parts = split("\|",$capturedHTML);
		if (count($parts)>2)
   	{
   		$parts[2]="";
   		$capturedHTML="";
   		$capturedHTML=$capturedHTML.$parts[6]."|".$parts[3];
   		//for ($i=1;$i<count($parts)-1;$i++) 
   		//{
   		//		$capturedHTML=$capturedHTML.$parts[$i]."|";		
     	//}
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
//	get163Quote("$symbols[$i]");
	$codelist=$_GET['code'];
	$parts = split("\|",$codelist);
	for ($i=0;$i<count($parts);$i++)
	{
		$code=$parts[$i];
		get163Quote("$code");
		if($i!=count($parts)-1)
		{
			echo ";";
		}
	} 
//} 
?> 

