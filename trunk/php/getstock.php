<? 
function get163Quote($stockSymbol = "000001") 
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

//����Ϊץȡ��һ������ 
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

