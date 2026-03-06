use minifb::{Key, Window, WindowOptions};

const W: usize = 320;
const H: usize = 240;

fn rot(x:f32,y:f32,z:f32,a:f32)->(f32,f32,f32){
let s=a.sin();let c=a.cos();
(x*c-z*s,y,x*s+z*c)
}

fn proj(x:f32,y:f32,z:f32)->(i32,i32){
let d=3.0/(z+4.0);
((x*d*120.0+160.0)as i32,(y*d*120.0+120.0)as i32)
}

fn main(){
let mut buf=vec![0u32;W*H];
let mut w=Window::new("Neopunk 3D Illusion",W,H,WindowOptions::default()).unwrap();
let cube=[
(-1.,-1.,-1.),(1.,-1.,-1.),(1.,1.,-1.),(-1.,1.,-1.),
(-1.,-1.,1.),(1.,-1.,1.),(1.,1.,1.),(-1.,1.,1.)
];
let edges=[(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)];
let mut t=0.0f32;
while w.is_open()&&!w.is_key_down(Key::Escape){
buf.fill(0);
let mut p=[(0,0);8];
for i in 0..8{
let(x,y,z)=cube[i];
let(a,b,c)=rot(x,y,z,t);
let(d,e,f)=rot(a,b,c,t*0.7);
p[i]=proj(d,e,f);
}
for&(i,j)in&edges{
let(x0,y0)=p[i];
let(x1,y1)=p[j];
let dx=(x1-x0).abs();
let dy=(y1-y0).abs();
let sx=if x0<x1{1}else{-1};
let sy=if y0<y1{1}else{-1};
let mut err=dx-dy;
let(mut x,mut y)=(x0,y0);
loop{
if x>=0&&y>=0&&(x as usize)<W&&(y as usize)<H{
buf[y as usize*W+x as usize]=0x00FF88;
}
if x==x1&&y==y1{break;}
let e2=2*err;
if e2>-dy{err-=dy;x+=sx;}
if e2<dx{err+=dx;y+=sy;}
}
}
w.update_with_buffer(&buf,W,H).unwrap();
t+=0.02;
}
}
