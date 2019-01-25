with Ada.Text_IO; use Ada.Text_IO;

with Lib2_Config;

package body Lib2 is
   procedure Print_Config is
   begin
      Put_Line ("Lib2: URL:" & Lib2_Config.url);
      Put_Line ("Lib2: Verbose:" & Lib2_Config.verbose'Img);
   end Print_Config;
end Lib2;
