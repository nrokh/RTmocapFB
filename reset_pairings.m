close all
clearvars
clc 
load("setPairings2_old.mat")
setPairings3 = zeros(size(setPairings2));
setPairings3(:,3) = setPairings2(:,3);

for i = 1:size(setPairings2,1)
    for j = 1:2
        if setPairings2(i,j) == 330
            setPairings3(i,j) = 300;
        elseif setPairings2(i,j) == 240
            setPairings3(i,j) = 270;
        elseif setPairings2(i,j) == 150
            setPairings3(i,j) = 220;
        elseif setPairings2(i,j) == 420
            setPairings3(i,j) = 330;
        elseif setPairings2(i,j) == 510
            setPairings3(i,j) = 380;
        else 
            setPairings3(i,j) = setPairings2(i,j);
        end
    end
end

save("setPairings2.mat", "setPairings3");