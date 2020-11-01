import javax.swing.JFrame;
import javax.swing.JPanel;
import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.awt.image.*;
import javax.imageio.*;

public class Game{

    public static void main(String[] args) {
	JFrame fr = new JFrame("Tile-based game");

	fr.setSize(600,600);
	fr.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	fr.getContentPane().setBackground(new Color(0,0,0));

	TileBasedGamePanel panel = new TileBasedGamePanel();
	panel.setOpaque(false);
	fr.add(panel);
  fr.setVisible(true);
    }
}
class TileBasedGamePanel extends JPanel implements KeyListener,Runnable {

    private char map[][];
    private int MX=11,MY=11;
    private String map_str[]=
//初期位置はa,b,cの順になりトロフィーの場所も1,2,3の順になる
//BがブロックLがはしご
    {"BcBBBaBBBbB",
     "B         B",
     "BBLBLBBBLBB",
     "B L L   L B",
     "BBBLBBLBBLB",
     "B  L  L  LB",
     "BLBBLBBLBBB",
     "BL  L  L  B",
     "BBLBBBLBLBB",
     "B2L  1L L3B",
     "BBBBBBBBBBB"};

    private Image boyImg,girlImg;
    private int boy_x,boy_y;
    private int girl1_x,girl2_x,girl3_x,girl11_x;
    private int gamen;
    private RoboCupTrophy trophy;
    private long dt0;
    private boolean hasTrophy=false;
    private boolean gameover=false;
    private boolean hasGirl=false;
    private Thread th;
    private int x1=110,ax1=10,x2=150,ax2=20,x3=190,ax3=40,x11=430,ax11=10,x22=390,ax22=20,x33=350,ax33=40;
    private int boy_xx,boy_yy;

    double time;

    TileBasedGamePanel(){
	gamen=0;
	th=new Thread(this);
	th.start();
	try{
	    File hikoboshiFile=new File("./hikoboshi.gif");
	    File orihimeFile=new File("./orihime.gif");
	    boyImg=ImageIO.read(hikoboshiFile);
	    girlImg=ImageIO.read(orihimeFile);
	}catch(IOException e){
	    System.err.println();
	}

	map=new char[MY+2][MX+2];

	for(int x=0;x<=MX+1;x++){
	    map[0][x]='B';
	    map[MY+1][x]='B';
        }

	for(int y=0;y<=MY+1;y++){
	    map[y][0]='B';
	    map[y][MX+1]='B';
	}

	for (int y = 1; y <= MY; y++) {
	    for (int x = 1; x <= MX; x++) {
		map[y][x] = map_str[y-1].charAt(x-1);
		if(map[y][x]=='M'){
		    boySet(x,y);
		}
	    }
	}


	trophy=new RoboCupTrophy(getSize(),0);
	addKeyListener(this);
	setFocusable(true);
    }
    @Override
	public void paintComponent(Graphics g) {
  if(gamen==0){
	    hasTrophy=false;
	    hasGirl=false;
	    g.setColor(Color.black);
	    g.fillRect(0,0,800,600);
	    g.setFont(new Font("TimeRoman", Font.BOLD, 60));
	    g.setColor(Color.white);
	    //g.drawString("TOP",210,100);
	    g.drawString("enterを押したら", 50, 200);
	    g.drawString("LEVEL1 START",50,350);
	    g.fillRect(20,430,570,100);
	    g.setFont(new Font("TimeRoman", Font.BOLD, 28));
            g.setColor(Color.black);
	    g.drawString("織姫から逃げてトロフィーをゲットしよう!",20,500);
	}
//LEVEL1画面
	    if(gamen==1){
		int dt = 30-(int) (0.001f*(System.currentTimeMillis()-dt0));
		if(dt>=0){
		g.setFont(new Font("TimeRoman", Font.BOLD, 18));
		g.setColor(Color.orange);
		g.drawString("limittime: " + dt, 55,30);
		g.drawString("LEVEL1",250,30);
		for (int y = 1; y <= MY; y++) {
		    for (int x = 1; x <= MX; x++) {
		int xx = 40*x+20, yy = 40*y+20;
		switch ( map[y][x] ) {
      case 'L': g.setColor(Color.white);
		    g.fillRect(xx+4, yy, 4, 40);
		    g.fillRect(xx+32, yy, 4, 40);
		    g.fillRect(xx+8, yy+8, 24, 4);
		    g.fillRect(xx+8, yy+28, 24, 4);
		    break;

//LEVEL1ではB,b,cの時ブロック
		case 'B':
    case'b':
    case'c':
    g.setColor(Color.darkGray);
		    g.fillRect(xx, yy, 26, 10);
		    g.fillRect(xx+32, yy, 8, 10);
		    g.fillRect(xx, yy+15, 10, 10);
		    g.fillRect(xx+16, yy+15, 24, 10);
		    g.fillRect(xx, yy+30, 18, 10);
		    g.fillRect(xx+24, yy+30, 16, 10);
		    break;

		case '1':trophy.setPosition(xx+20,yy+20);
		}
		    }
		}
	    trophy.draw(g);
	    trophy.rotate();
	    boyDraw(g);

//敵の初期位置
	    for(int i=1;i<4;i++){
		g.drawImage(girlImg,x1,80*(2*i-1)+20,this);
	     }
       for(int j=1;j<3;j++){
 		g.drawImage(girlImg,x11,80*2*j+20,this);
 	     }



//トロフィー取ったら
	    if(hasTrophy){
		gamen=2;
	    }
//敵に当たったら、時間オーバーだったら
	    if(hasGirl || dt==0){
		gamen=6;
	    }
		}
	    }

//LEVEL1クリアでLEVEL2の間
	    if(gamen==2){
		hasTrophy=false;
		g.setColor(Color.black);
                g.fillRect(0,0,800,600);
                g.setFont(new Font("TimeRoman", Font.BOLD, 70));
                g.setColor(Color.white);
                g.drawString("LEVEL1 Clear!", 30, 300);
                g.setFont(new Font("TimeRoman",Font.BOLD,40));
                g.drawString("enterを押したらLEVEL2へ",20,450);
	    }
//LEVEL2
	    if(gamen==3){
                int dt = 30-(int) (0.001f*(System.currentTimeMillis()-dt0));
                if(dt>0){
		    g.setFont(new Font("TimeRoman", Font.BOLD, 18));
		    g.setColor(Color.orange);
		    g.drawString("limittime: " + dt, 55,30);
		    g.drawString("LEVEL2",250,30);
		    for (int y = 1; y <= MY; y++) {
			for (int x = 1; x <= MX; x++) {
			    int xx = 40*x+20, yy = 40*y+20;
			    switch ( map[y][x] ) {

			    case 'L': g.setColor(Color.white);
				g.fillRect(xx+4, yy, 4, 40);
				g.fillRect(xx+32, yy, 4, 40);
				g.fillRect(xx+8, yy+8, 24, 4);
				g.fillRect(xx+8, yy+28, 24, 4);
				break;

			    case 'B':
          case 'a':
          case'c':
        g.setColor(Color.darkGray);
				g.fillRect(xx, yy, 26, 10);
				g.fillRect(xx+32, yy, 8, 10);
				g.fillRect(xx, yy+15, 10, 10);
				g.fillRect(xx+16, yy+15, 24, 10);
				g.fillRect(xx, yy+30, 18, 10);
				g.fillRect(xx+24, yy+30, 16, 10);
				break;

			    case'2':trophy.setPosition(xx+20,yy+20);
			    }
			}
		    }
		    trophy.draw(g);
		    trophy.rotate();
		    boyDraw(g);
//敵の初期位置
for(int i1=1;i1<4;i1++){
g.drawImage(girlImg,x1,80*(2*i1-1)+20,this);
 }
 for(int j1=1;j1<3;j1++){
g.drawImage(girlImg,x11,80*2*j1+20,this);
 }
 for(int i2=1;i2<4;i2++){
g.drawImage(girlImg,x2,80*(2*i2-1)+20,this);
  }
  for(int j2=1;j2<3;j2++){
g.drawImage(girlImg,x22,80*2*j2+20,this);
  }

		    if(hasTrophy){
			gamen=4;
		    }

		    if(hasGirl||dt==0){
			gamen=6;
		    }
                }
            }
  //LEVEl2クリアからLEVEL3への間
	    if(gamen==4){
                hasTrophy=false;
                g.setColor(Color.black);
                g.fillRect(0,0,800,600);
                g.setFont(new Font("TimeRoman", Font.BOLD, 70));
                g.setColor(Color.white);
                g.drawString("LEVEL2 Clear!", 30, 300);
                g.setFont(new Font("TimeRoman",Font.BOLD,40));
                g.drawString("enterを押したらLEVEL3へ",20,450);
}

//LEVEL3
	    if(gamen==5){
                int dt = 30-(int) (0.001f*(System.currentTimeMillis()-dt0));

                if(dt>=0){
                    g.setFont(new Font("TimeRoman", Font.BOLD, 18));
                    g.setColor(Color.orange);
                    g.drawString("limittime: " + dt, 55,30);
                    g.drawString("LEVEL3",250,30);
                    for (int y = 1; y <= MY; y++) {
			                   for (int x = 1; x <= MX; x++) {
                            int xx = 40*x+20, yy = 40*y+20;
                            switch ( map[y][x] ) {
                            case 'L': g.setColor(Color.white);
                                g.fillRect(xx+4, yy, 4, 40);
                                g.fillRect(xx+32, yy, 4, 40);
                                g.fillRect(xx+8, yy+8, 24, 4);
                                g.fillRect(xx+8, yy+28, 24, 4);
                                break;

                            case 'B':
                            case'a':
                            case'b':
                            g.setColor(Color.darkGray);
                                g.fillRect(xx, yy, 26, 10);
                                g.fillRect(xx+32, yy, 8, 10);
                                g.fillRect(xx, yy+15, 10, 10);
                                g.fillRect(xx+16, yy+15, 24, 10);
                                g.fillRect(xx, yy+30, 18, 10);
                                g.fillRect(xx+24, yy+30, 16, 10);
                                break;

			    case '3':trophy.setPosition(xx+20,yy+20);
                            }
                        }
                    }
                    trophy.draw(g);
                    trophy.rotate();
                    boyDraw(g);
//敵配置
for(int i1=1;i1<4;i1++){
g.drawImage(girlImg,x1,80*(2*i1-1)+20,this);
 }
 for(int j1=1;j1<3;j1++){
g.drawImage(girlImg,x11,80*2*j1+20,this);
 }
 for(int i2=1;i2<4;i2++){
g.drawImage(girlImg,x2,80*(2*i2-1)+20,this);
  }
  for(int j2=1;j2<3;j2++){
g.drawImage(girlImg,x22,80*2*j2+20,this);
}for(int i3=1;i3<4;i3++){
  g.drawImage(girlImg,x3,80*(2*i3-1)+20,this);
   }
   for(int j3=1;j3<3;j3++){
  g.drawImage(girlImg,x33,80*2*j3+20,this);
   }



    //トロフィーとる
                    if(hasTrophy){
                        gamen=7;
                    }
                    if(hasGirl ||dt==0){
                        gamen=6;
                    }
                }
		}
//ゲームオーバー画面
	    if(gamen==6){
		g.setColor(Color.black);
		g.fillRect(0,0,800,600);
		g.setFont(new Font("TimeRoman", Font.BOLD, 90));
		g.setColor(Color.red);
		g.drawString("Game Over!", 0, 300);
		g.setFont(new Font("TimeRoman",Font.BOLD,40));
		g.drawString("enterを押したらTOPへ",45,450);
	    }
//クリア画面
	    if(gamen==7){
		g.setColor(Color.black);
		g.fillRect(0,0,800,600);
		g.setFont(new Font("TimeRoman", Font.BOLD, 60));
		g.setColor(Color.white);
		g.drawString("Congratulations!",0,200);
		g.drawString("Game Clear!!", 80, 300);
		g.setFont(new Font("TimeRoman", Font.BOLD, 40));
		g.drawString("enterを押したらTOPへ",50,450);
	    }
    }
    public void run(){
	while(th!=null){
	    x1=x1 + ax1;
      x11=x11+ax11;
	    x2= x2 + ax2;
      x22=x22+ax22;
	    x3=x3+ax3;
      x33=x33+ax33;
      boy_xx=40*boy_x+30;
      boy_yy=40*boy_y+20;

	    if(x1 < 110 || x1 > 430  ) {ax1 = -ax1; x1 += 2 * ax1;};
      if(x11 < 110 || x11 > 430) {ax11= -ax11; x11 += 2 *ax11;};
	    if(x2 < 110  || x2 > 430  ) {ax2 = -ax2; x2 += 2 * ax2;};
      if(x22 < 110  || x22 > 430  ) {ax22 = -ax22; x22 += 2 * ax22;};
	    if(x3 < 110 || x3 > 430) {ax3= -ax3; x3 += 2 *ax3;};
      if(x33 < 110  || x33 > 430  ) {ax33 = -ax33; x33 += 2 * ax33;};
      //(x11-20)/40

	    if(gamen==1){
        if(map[boy_y][boy_x]=='1'){
     getItem();
       }
       if((boy_y%2==0&&boy_y%4!=0&&boy_xx==x1)||(boy_y%2==0&&boy_y%4==0&&boy_xx==x11)){
            getGirl();
       }
		}
	    if(gamen==3){
        if(map[boy_y][boy_x]=='2'){
     getItem();
       }
        if((boy_y%2==0&&boy_y%4!=0&&boy_xx==x1)||(boy_y%2==0&&boy_y%4==0&&boy_xx==x11)||
        (boy_y%2==0&&boy_y%4!=0&&boy_xx==x2)||(boy_y%2==0&&boy_y%4==0&&boy_xx==x22)){
			getGirl();
		    }
		}
	    if(gamen==5){
        if(map[boy_y][boy_x]=='3'){
        getItem();
        }
        if((boy_y%2==0&&boy_y%4!=0&&boy_xx==x1)||(boy_y%2==0&&boy_y%4==0&&boy_xx==x11)||
        (boy_y%2==0&&boy_y%4!=0&&boy_xx==x2)||(boy_y%2==0&&boy_y%4==0&&boy_xx==x22)||
        (boy_y%2==0&&boy_y%4!=0&&boy_xx==x3)||(boy_y%2==0&&boy_y%4==0&&boy_xx==x33))
        getGirl();

                }
	    repaint();{


		try{
		    th.sleep(100);}
		catch(InterruptedException e){}
	    }
	}
    }
    //
    @Override
	public void keyPressed(KeyEvent e) {
	int key =e.getKeyCode();
	int dir =-1;

	switch (key) {
	case KeyEvent.VK_LEFT: dir = 2; break;
	case KeyEvent.VK_RIGHT: dir = 0; break;
	case KeyEvent.VK_UP: dir = 1; break;
	case KeyEvent.VK_DOWN: dir = 3; break;
	case KeyEvent.VK_ENTER:change();break;
	}
	if ( dir >= 0 )
	    boyMove(dir);
	repaint();
    }

    @Override
	public void keyReleased(KeyEvent e) { }

    @Override
	public void keyTyped(KeyEvent e) { }
    //

    public void change(){
	if(gamen==0)
	    {
		gamen=1;
		boy_x=boy_x*0+6;
		boy_y=boy_y*0+1;
		repaint();

		dt0=System.currentTimeMillis();
		return;
	    }

	if(gamen==2)
	    {gamen=3;
		boy_x=boy_x*0+10;
		boy_y=boy_y*0+1;
		repaint();
		dt0=System.currentTimeMillis();
		return;
	    }
	if(gamen==4)
	    {gamen=5;
		boy_x=boy_x*0+2;
                boy_y=boy_y*0+1;
                repaint();
                dt0=System.currentTimeMillis();
                return;
	    }
	if(gamen==6||gamen==7){
	    gamen=0;
	}
    }
    //
    public void boySet(int x, int y) {
	boy_x = x;
	boy_y = y;
    }
    //
    //
    public void boyDraw(Graphics g) {
	g.drawImage(boyImg, boy_xx,boy_yy, this);
  //System.out.println(x1);
  //  System.out.println(boy_xx);
    }
    //
    public void boyMove(int dir) {
	int dx = 0, dy = 0;
	switch ( dir ) {
	case 0: dx =  1; break;
	case 1: dy = -1; break;
	case 2: dx = -1; break;
	case 3: dy =  1; break;
	}
	if ( dx == 0 && dy == 0 ) return;

	if ( map[boy_y+dy][boy_x+dx] == 'B' )
	    return;
	boy_x += dx; boy_y += dy;
    }

    public void getItem() {
	hasTrophy = true;
    }
    //
    public void getGirl(){
    	hasGirl=true;
    }

}
//王冠の動き
class RoboCupTrophy {

    private int[] xx =
    {5, 20, 30, 35, 30, 15, 30, 10, 15, 20};
    private int[] yy =
    {-60, -55, -40, -30, -20, -10, -25, 25, 35, 50};
    private double[][] x = new double[10][10];
    private double[][] y = new double[10][10];
    private double[][] z = new double[10][10];
    private double alpha = Math.PI/90;
    private double beta  = Math.PI/90;
    private double gamma = Math.PI/90;
    private double delta = Math.PI/5;
    private Dimension s;
    protected int n;
  private int offset_x, offset_y;
    RoboCupTrophy(Dimension s, int n) {
	this.s = s; this.n = 1;
	for (int i=0; i<10; i++) {
      x[0][i] = xx[i];
      y[0][i] = yy[i];
      z[0][i] = 0;
    }
    double x1, z1;
    for (int i=0; i<9; i++)
      for (int j=0; j<10; j++) {
	x1 = x[i][j]; z1 = z[i][j];
	x[i+1][j] = x1*Math.cos(delta)+
	            z1*Math.sin(delta);
	y[i+1][j] = y[i][j];
	z[i+1][j] = -x1*Math.sin(delta)+
	            z1*Math.cos(delta);
      }
    }

public void setPosition(int x, int y) {
    offset_x = x;
    offset_y = y;
  }

  public void draw(Graphics g) {
    g.setColor(Color.yellow);
    int h = n / 3; int v = n % 3;
    int x1, y1, x2, y2;
    int wu = s.width/3;
    int hu = s.height/4;

    for (int i=0; i<10; i++)
      for (int j=0; j<10; j++) {
	x1 = (int)(x[i][j]/3)+(h+1)*wu;
	y1 = (int)(y[i][j]/3)+(v+1)*hu;
	x2 = (int)(x[(i+1)%10][j]/3)+(h+1)*wu;
	y2 = (int)(y[(i+1)%10][j]/3)+(v+1)*hu;
	g.drawLine(x1+offset_x,y1+offset_y,x2+offset_x,y2+offset_y);
      }
    for (int i=0; i<10; i++)
      for (int j=0; j<9; j++) {
	x1 = (int)(x[i][j]/3)+(h+1)*wu;
	y1 = (int)(y[i][j]/3)+(v+1)*hu;
	x2 = (int)(x[i][(j+1)%10]/3)+(h+1)*wu;
	y2 = (int)(y[i][(j+1)%10]/3)+(v+1)*hu;
	g.drawLine(x1+offset_x,y1+offset_y,x2+offset_x,y2+offset_y);
      }
    }

  public void rotate() {
    double x1,x2,x3,y1,y2,y3,z1,z2;
    for (int i=0; i<10; i++)
      for (int j=0; j<10; j++) {
	x1 = x[i][j]; y1 = y[i][j];
	z1 = z[i][j]; x2 = x1;
	y2 = y1*Math.cos(alpha)-z1*Math.sin(alpha);
	z2 = y1*Math.sin(alpha)+z1*Math.cos(alpha);
	x3 = x2*Math.cos(beta)+z2*Math.sin(beta);
	y3 = y2;
	x[i][j] = x3*Math.cos(gamma)-y3*Math.sin(gamma);
	y[i][j] = x3*Math.sin(gamma)+y3*Math.cos(gamma);
	z[i][j] = -x2*Math.sin(beta)+z2*Math.cos(beta);
      }
  }
}
