%% 第二问第一部分熵权法
clc;clear;
load data
score=data;
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
s_chaoyang = s(1);
% [ss,rank]=sort(s,'descend'); 