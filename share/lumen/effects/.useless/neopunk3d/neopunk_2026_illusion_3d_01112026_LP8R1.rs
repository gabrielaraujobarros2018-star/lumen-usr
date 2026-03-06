use minifb::{Key, Window, WindowOptions};

const W: usize = 300;
const H: usize = 300;

fn rotz(x:f32,y:f32,a:f32)->(f32,f32){
(x*a.cos()-y*a.sin(),x*a.sin()+y*a.cos())
}

fn main(){
let mut b=vec![0u32;W*H];
let mut w=Window::new("Neopunk Ring",W,H,WindowOptions::default()).unwrap();
let mut t=0.0f32;
while w.is_open()&&!w.is_key_down(Key::Escape){
b.fill(0);
for i in 0..360{
let a=i as f32*0.0174;
let(r1,r2)=(1.2,0.4);
let(x,y)=rotz((r1+r2*(a*3.0+t).cos())*a.cos(),(r1+r2*(a*3.0+t).cos())*a.sin(),t);
let z=r2*(a*3.0+t).sin();
let d=2.5/(z+3.5);
let px=(x*d*100.0+150.0)as i32;
let py=(y*d*100.0+150.0)as i32;
if px>=0&&py>=0&&(px as usize)<W&&(py as usize)<H{
b[py as usize*W+px as usize]=0x22FFCC;
}
}
w.update_with_buffer(&b,W,H).unwrap();
t+=0.02;
}
}