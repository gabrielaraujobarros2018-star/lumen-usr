use minifb::{Key, Window, WindowOptions};

const W: usize = 360;
const H: usize = 260;

fn spin(p:(f32,f32,f32),a:f32)->(f32,f32,f32){
let(s,c)=(a.sin(),a.cos());
(p.0*c-p.2*s,p.1,p.0*s+p.2*c)
}

fn proj(p:(f32,f32,f32))->(i32,i32){
let d=2.8/(p.2+5.0);
((p.0*d*140.0+180.0)as i32,(p.1*d*140.0+130.0)as i32)
}

fn main(){
let mut fb=vec![0u32;W*H];
let mut win=Window::new("Neopunk Illusion",W,H,WindowOptions::default()).unwrap();
let pts=[(-1.,-1.,0.),(1.,-1.,0.),(1.,1.,0.),(-1.,1.,0.)];
let mut a=0.0;
while win.is_open()&&!win.is_key_down(Key::Escape){
fb.fill(0);
let mut pp=[(0,0);4];
for i in 0..4{
let r=spin(pts[i],a);
pp[i]=proj(r);
}
for i in 0..4{
let(x0,y0)=pp[i];
let(x1,y1)=pp[(i+1)%4];
let mut x=x0;
let mut y=y0;
let dx=(x1-x0).signum();
let dy=(y1-y0).signum();
while x!=x1||y!=y1{
if x>=0&&y>=0&&(x as usize)<W&&(y as usize)<H{
fb[y as usize*W+x as usize]=0x8844FF;
}
x+=dx;y+=dy;
}
}
win.update_with_buffer(&fb,W,H).unwrap();
a+=0.03;
}
}