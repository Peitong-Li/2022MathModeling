%% 第二问第一部分熵权法
clc;clear;
load './data/data'
region_index = 1;
a1_p = data(1,1);
a2_p = data(2,1);
a3_p = data(3,1);
a4_p = data(4,1);
a5_p = data(5,1);
a6_p = data(6,1);
a7_p = data(7,1);
a8_p = data(8,1);
a9_p = data(9,1);
for a1=fliplr(15:16)
%     score=data([1 region_index], :);
    for a2=fliplr(8:10)
        for a3=fliplr(15:20)
            for a4=fliplr(15:20)
                for a5=fliplr(15:20)
                    for a6=fliplr(5:10)
                        for a7=fliplr(15:20)
                            for a8=fliplr(5:10)
                                for a9=10:fliplr(5:10)
                                    score=data;
                                    score(1,9)=a1;
                                    score(2,9)=a2;
                                    score(3,9)=a3;
                                    score(4,9)=a4;
                                    score(5,9)=a5;
                                    score(6,9)=a6;
                                    score(7,9)=a7;
                                    score(8,9)=a8;
                                    score(9,9)=a9;
                                    [n,m]=size(score);
                                    score2=zeros(n,m);
                                    for j=1:m
                                        for i=1:n
                                            score2(i,j)=(score(i,j)-min(score(:,j)))/(max(score(:,j))-min(score(:,j)));
                                            if score2(i,j)==0
                                                score2(i,j)=0.0001; 
                                            end
                                        end
                                    end
                                    for i=1:n
                                        p(i,:)=score2(i,:)./sum(score2);
                                    end
                                    e=-sum(p.*log(p))/log(n);       
                                    g=1-e; 
                                    % g = e;
                                    w=g/sum(g); 
                                    s=w*p'; 
                                    [ss,rank]=sort(s,'descend');
                                    fprintf("%d,%d,%d,%d,%d,%d,%d,%d,%d\n",a1,a2,a3,a4,a5,a6,a7,a8,a9);
                                    if rank(1)~=1 && rank(1)~=5
                                        disp(rank(1));
                                        fprintf("--%d--,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n",rank(1),a1,a2,a3,a4,a5,a6,a7,a8,a9)
                                        return
                                    end
                                end
                            end
                        end
                    end
                end
            end
        end
    end
end
