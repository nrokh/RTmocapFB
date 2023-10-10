function [leftNums, rightNums] = findMarkerNums(input_struct)

Lcal_num = [ 3*find(matches(input_struct.labels, 'LCAL'),1)-2, 3*find(matches(input_struct.labels, 'LCAL'),1)-1, 3*find(matches(input_struct.labels, 'LCAL'),1)];
Lsac_num = [ 3*find(matches(input_struct.labels, 'LPSI'),1)-2, 3*find(matches(input_struct.labels, 'LPSI'),1)-1, 3*find(matches(input_struct.labels, 'LPSI'),1)];
L2mt_num = [ 3*find(matches(input_struct.labels, 'L2MT'),1)-2, 3*find(matches(input_struct.labels, 'L2MT'),1)-1, 3*find(matches(input_struct.labels, 'L2MT'),1)];
Lmep_num = [ 3*find(matches(input_struct.labels, 'LMEP'),1)-2, 3*find(matches(input_struct.labels, 'LMEP'),1)-1, 3*find(matches(input_struct.labels, 'LMEP'),1)];
Llep_num = [ 3*find(matches(input_struct.labels, 'LLEP'),1)-2, 3*find(matches(input_struct.labels, 'LLEP'),1)-1, 3*find(matches(input_struct.labels, 'LLEP'),1)];
Lasi_num = [ 3*find(matches(input_struct.labels, 'LASI'),1)-2, 3*find(matches(input_struct.labels, 'LASI'),1)-1, 3*find(matches(input_struct.labels, 'LASI'),1)];
Lpsi_num = [ 3*find(matches(input_struct.labels, 'LPSI'),1)-2, 3*find(matches(input_struct.labels, 'LPSI'),1)-1, 3*find(matches(input_struct.labels, 'LPSI'),1)];

Rcal_num = [ 3*find(matches(input_struct.labels, 'RCAL'),1)-2, 3*find(matches(input_struct.labels, 'RCAL'),1)-1, 3*find(matches(input_struct.labels, 'RCAL'),1)];
Rlml_num = [ 3*find(matches(input_struct.labels, 'RLML'),1)-2, 3*find(matches(input_struct.labels, 'RLML'),1)-1, 3*find(matches(input_struct.labels, 'RLML'),1)];
Rmml_num = [ 3*find(matches(input_struct.labels, 'RMML'),1)-2, 3*find(matches(input_struct.labels, 'RMML'),1)-1, 3*find(matches(input_struct.labels, 'RMML'),1)];
Rsac_num = [ 3*find(matches(input_struct.labels, 'RPSI'),1)-2, 3*find(matches(input_struct.labels, 'RPSI'),1)-1, 3*find(matches(input_struct.labels, 'RPSI'),1)];
R2mt_num = [ 3*find(matches(input_struct.labels, 'R2MT'),1)-2, 3*find(matches(input_struct.labels, 'R2MT'),1)-1, 3*find(matches(input_struct.labels, 'R2MT'),1)];
R1mt_num = [ 3*find(matches(input_struct.labels, 'R1MT'),1)-2, 3*find(matches(input_struct.labels, 'R1MT'),1)-1, 3*find(matches(input_struct.labels, 'R1MT'),1)];
R5mt_num = [ 3*find(matches(input_struct.labels, 'R5MT'),1)-2, 3*find(matches(input_struct.labels, 'R5MT'),1)-1, 3*find(matches(input_struct.labels, 'R5MT'),1)];
Rmep_num = [ 3*find(matches(input_struct.labels, 'RMEP'),1)-2, 3*find(matches(input_struct.labels, 'RMEP'),1)-1, 3*find(matches(input_struct.labels, 'RMEP'),1)];
Rlep_num = [ 3*find(matches(input_struct.labels, 'RLEP'),1)-2, 3*find(matches(input_struct.labels, 'RLEP'),1)-1, 3*find(matches(input_struct.labels, 'RLEP'),1)];
Rasi_num = [ 3*find(matches(input_struct.labels, 'RASI'),1)-2, 3*find(matches(input_struct.labels, 'RASI'),1)-1, 3*find(matches(input_struct.labels, 'RASI'),1)];
Rpsi_num = [ 3*find(matches(input_struct.labels, 'RPSI'),1)-2, 3*find(matches(input_struct.labels, 'RPSI'),1)-1, 3*find(matches(input_struct.labels, 'RPSI'),1)];

leftNums = {"LCAL",[Lcal_num];"LSAC",[Lsac_num]; "L2MT",[L2mt_num]; "LMEP",[Lmep_num]; "LLEP",[Llep_num]; "LASI",[Lasi_num]; "LPSI",[Lpsi_num]};
rightNums = {"RCAL",[Rcal_num];"RSAC", [Rsac_num];"R2MT",[R2mt_num]; "RMEP",[Rmep_num];"RLEP", [Rlep_num];"RASI", [Rasi_num]; "RPSI",[Rpsi_num]; "RLML",[Rlml_num]; "RMML",[Rmml_num]; "R1MT", [R1mt_num];"R5MT", [R5mt_num]};


end