with Ada.Text_IO; use Ada.Text_IO;

with Lib1_Config;

package body Lib1 is
   procedure Print_Config is
   begin
      Put_Line ("Lib1: Max_Path_Len:" & Lib1_Config.max_path_len'Img);
      Put_Line ("Lib1: Verbose:" & Lib1_Config.verbose'Img);
   end Print_Config;
end Lib1;
