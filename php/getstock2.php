<? 
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
