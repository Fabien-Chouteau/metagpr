with Ada.Text_IO;

with Lib1;
with Lib2;
with Lib3;

procedure main is
begin
   Ada.Text_IO.Put_Line ("Hello from app");
   Lib1.Print_Config;
   Lib2.Print_Config;
   Lib3.Print_Config;
end main;
