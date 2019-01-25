with Ada.Text_IO; use Ada.Text_IO;

with Lib3_Config;

package body Lib3 is
   procedure Print_Config is
   begin
      Put_Line ("Lib3: Verbose:" & Lib3_Config.verbose'Img);
   end Print_Config;
end Lib3;
