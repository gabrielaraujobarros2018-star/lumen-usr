use minifb::{Key, Window, WindowOptions};

const W: usize = 320;
const H: usize = 200;

fn main(){
let mut f=vec![0u32;W*H];
let mut w=Window::new("Neopunk Vortex",W,H,WindowOptions::default()).unwrap();
let mut t=0.0f32;
while w.is_open()&&!w.is_key_down(Key::Escape){
for y in 0..H{
for x in 0..W{
let fx=x as f32-160.0;
let fy=y as f32-100.0;
let d=(fx*fx+fy*fy).sqrt();
let a=fy.atan2(fx)+t;
let v=((a.sin()*0.5+0.5)*(255.0-d)).max(0.0)as u32;
f[y*W+x]=(v<<8)|v;
}
}
w.update_with_buffer(&f,W,H).unwrap();
t+=0.04;
}
}