close all
clearvars
clc 
load("setPairings2_old.mat")
setPairings = setPairings2;
setPairings2 = zeros(size(setPairings));
setPairings2(:,3) = setPairings(:,3);

for i = 1:size(setPairings,1)
    for j = 1:2
        if setPairings(i,j) == 330
            setPairings2(i,j) = 300;
        elseif setPairings(i,j) == 240
            setPairings2(i,j) = 270;
        elseif setPairings(i,j) == 150
            setPairings2(i,j) = 220;
        elseif setPairings(i,j) == 420
            setPairings2(i,j) = 330;
        elseif setPairings(i,j) == 510
            setPairings2(i,j) = 380;
        else 
            setPairings2(i,j) = setPairings(i,j);
        end
    end
end

save("setPairings2.mat", "setPairings2");