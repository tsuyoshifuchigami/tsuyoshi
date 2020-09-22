<body>
<?php
session_start();


$name_=$_POST["name"];
$comment_=$_POST["comment"];
$number=$_POST["number"];
$number2=$_POST["number2"];
$hidden1=$_POST["hidden1"];
$pass_=$_POST["pass"];

##
$dsn='データベース名';
$user='ユーザー名';
$password='パスワード';
##

$pdo=new PDO($dsn,$user,$password,array(PDO::ATTR_ERRMODE => 
PDO::ERRMODE_WARNING));

$sql = "CREATE TABLE IF NOT EXISTS tbtest"
	." ("
	. "id INT AUTO_INCREMENT PRIMARY KEY,"
	. "name char(32),"
	. "comment TEXT,"
	. "date TEXT,"
	. "pass TEXT"
	.");";
	$stmt = $pdo->query($sql);

#投稿
if ((isset($_REQUEST["chkno"]) == true) && (isset($_SESSION["chkno"]) == true)
	 && ($_REQUEST["chkno"] == $_SESSION["chkno"]))	// トークン番号が一致？
	{

if(!empty($name_)&&!empty($comment_)
&&empty($hidden1)&&!empty($_POST["submit1"])){
$sql = $pdo -> prepare("INSERT INTO tbtest (name,comment,date,pass) 
VALUES (:name,:comment,:date,:pass)");
	$sql -> bindParam(':name', $name, PDO::PARAM_STR);
	$sql -> bindParam(':comment', $comment, PDO::PARAM_STR);
	$sql -> bindParam(':date', $date, PDO::PARAM_STR);
    $sql -> bindParam(':pass', $pass, PDO::PARAM_STR);
	$name = $name_;
	$comment = $comment_; //好きな名前、好きな言葉は自分で決めること
	$date=date("Y/m/d H:i:s");
	$pass=$pass_;
	$sql -> execute();
}#if文とじ


#編集後投稿
if(!empty($name_)&&!empty($comment_)
&&!empty($hidden1)&&!empty($_POST["submit1"])){
    $id =$hidden1; //変更する投稿番号
	$name =$name_;
	$comment =$comment_; //変更したい名前、変更したいコメントは自分で決めること
	$date=date("Y/m/d H:i:s");
	$pass=$pass_;
	
	$sql = 'UPDATE tbtest SET name=:name,comment=:comment,
	date=:date,pass=:pass WHERE id=:id';
	$stmt = $pdo->prepare($sql);
	$stmt->bindParam(':name', $name, PDO::PARAM_STR);
	$stmt->bindParam(':comment', $comment, PDO::PARAM_STR);
	$stmt->bindParam(':date', $date, PDO::PARAM_STR);
	$stmt->bindParam(':pass', $pass, PDO::PARAM_STR);
	$stmt->bindParam(':id', $id, PDO::PARAM_INT);
	$stmt->execute();
}



#編集
if(!empty($number2)&&!empty($_POST["submit3"])){
    $sql = 'SELECT * FROM tbtest';
	$stmt = $pdo->query($sql);
	$results = $stmt->fetchAll();
    foreach ($results as $row){
        if($number2==$row['id']&&$pass_==$row['pass']){
                $aa=$row['name'];
                $bb=$row['comment'];
                $cc=$row['pass'];
            
    }
    }
}



#削除
if(!empty($number)&&!empty($_POST["submit2"])){
    $sql = 'SELECT * FROM tbtest';
	$stmt = $pdo->query($sql);
	$results = $stmt->fetchAll();
	foreach ($results as $row){
	    if($number==$row['id']&&$pass_==$row['pass']){
        $id = $number;
	    $sql = 'delete from tbtest where id=:id';
	    $stmt = $pdo->prepare($sql);
	    $stmt->bindParam(':id', $id, PDO::PARAM_INT);
	    $stmt->execute();
}
}
}


}
$_SESSION["chkno"]=$chkno=mt_rand();
?>

<form action=""method="post">
        <input type="password" name="pass"
        placeholder="パスワード"required
        value="<?php if(!empty($number2)){echo$cc;}?>"><br> 
        <input type="text"name="name"placeholder="名前"
        value="<?php if(!empty($number2)){echo$aa;}?>">
        <input type="text"name="comment"placeholder="コメント"
        value="<?php if(!empty($number2)){echo$bb;}?>">
        <input type="submit"name="submit1">
        <br>
        <input type="number"name="number"placeholder="削除対象番号">
        <input type="submit"name="submit2" value="削除">
        <br>
        <input type="number"name="number2"placeholder="編集番号">
        <input type="submit"name="submit3" value="編集">
        
        <input type="hidden"name="hidden1"
        value="<?php echo$number2;?>">
        
        <input name="chkno" type="hidden" value="<?php echo $chkno; ?>">
</form>

<?php

#テーブル表示
    $sql = 'SELECT * FROM tbtest';
	$stmt = $pdo->query($sql);
	$results = $stmt->fetchAll();
	foreach ($results as $row){
		//$rowの中にはテーブルのカラム名が入る
		echo $row['id'].'<>';
		echo $row['name'].'<>';
		echo $row['comment'].'<>';
		echo $row['date'].'<>';
		echo $row['pass'].'<br>';
	echo "<hr>";
	}


#テーブル削除	
#$sql = 'DROP TABLE tbtest';
#$stmt = $pdo->query($sql);
?>

</body>
