<? 
function getSohuQuote($stockSymbol = "000001") 
{ 
if (!$targetURL) $targetURL = "http://stock.business.sohu.com/stock_image/realtime_table.php?code=$stockSymbol"; //�趨Ҫץȡ��URLĿ�� 
$fd = fopen("$targetURL", "r"); 
$stopExtract = 0; 
$startExtract = 0; 
while (!feof($fd)) 
{ 
	$buffer = fgets($fd, 4096); 
	
	if (!$startExtract)
	{
		if (strstr($buffer, "���")) 
		{ 
			$startExtract = 1; 
		}
	}
 
	if ($startExtract && !$stopExtract) 
	{ 
		$buffer = str_replace("</td>", "|", $buffer); 
		$buffer = str_replace("&nbsp;", "", $buffer); 
		$buffer = trim(strip_tags($buffer)); 
		if (strstr($buffer, "��")) 
		{ 
			$stopExtract = 1; 
		} 
		$capturedHTML .= $buffer; 
	} 
	if ($startExtract && strstr($buffer, "��")) 
	{ 
		$stopExtract = 1;
		$capturedHTML = str_replace("���", "", $capturedHTML); 
		$capturedHTML = str_replace("�ˣƣȣԣΣ�||", "", $capturedHTML); 
		$capturedHTML = str_replace("|��- ��������ͼ��- ��Ҫ����ָ���- ��ʷ�ɽ���ϸ��- ����ָ���- ������Ѷ��- ��������", "", $capturedHTML);  
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
