library(MASS)
library(ROCR)
require(car)



train<-read.csv('0816_9shiba20.csv', header=T, fileEncoding="Shift_JIS")
train_<-train[,c(75,24,25,26,27,28,29,30,35,40,41,42,43,44,53,54,55,50,59,60,61,62,63,67,68,69,70,71,73)]


lo<-read.csv('17_9shiba20.csv', header=T, fileEncoding="Shift_JIS")
lo_<-lo[,c(75,24,25,26,27,28,29,30,35,40,41,42,43,44,53,54,55,50,59,60,61,62,63,67,68,69,70,71,72,73,74)]


#64,65父
#c(75,8,9,10,11,12,13,14,15,16,17,18,19,20,21,24,25,26,27,28,29,30,31,35,36,37,39,40,41,42,43,44,45,46,47,48,49,50,53,54,55,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74)]

test<-read.csv('18_9shiba20.csv', header=T, fileEncoding="Shift_JIS")
test_<-test[,c(75,24,25,26,27,28,29,30,35,40,41,42,43,44,53,54,55,50,59,60,61,62,63,67,68,69,70,71,72,73,74)]


future<-read.csv('osaka.csv', header=T, fileEncoding="Shift_JIS")
future_<-future[,c(75,24,25,26,27,28,29,30,35,40,41,42,43,44,45,53,54,55,50,59,60,61,62,63,67,68,69,70,71,72,73,74)]
predict(ansaic,newdata=future_,type="response")

ans<- glm(train_$log_fuku~.,data=train_,family=binomial(link = "logit")) #解析結果をansに代入
summary(ans)


ansaic<-step(ans)


summary(ansaic)
#ansbic<-step(ans,k=log(nrow(train_)))2282

a<-predict(ansaic,newdata=lo_,type="response")
aa<-data.frame(a,lo_[1])
pred <- prediction(aa[,1], aa[,2])
perf <- performance(pred, "tpr", "fpr")
#plot(perf)
table <- data.frame(Cutoff=unlist(pred@cutoffs),
                    TP=unlist(pred@tp), FP=unlist(pred@fp),
                    FN=unlist(pred@fn), TN=unlist(pred@tn),
                    Sensitivity=unlist(pred@tp)/(unlist(pred@tp)+unlist(pred@fn)),
                    Specificity=unlist(pred@tn)/(unlist(pred@fp)+unlist(pred@tn)),
                    Accuracy=((unlist(pred@tp)+unlist(pred@tn))/nrow(lo_))
)

#table
max(table$Accuracy)
t<-which.max(table$Accuracy)
#t
kk<-table$Cutoff[t+1]

a1<-predict(ansaic,newdata=train_,type="response")
aa1<-data.frame(a1,train_[1])
pred1 <- prediction(aa1[,1], aa1[,2])
perf1 <- performance(pred1, "tpr", "fpr")
#plot(perf1)
table1 <- data.frame(Cutoff=unlist(pred1@cutoffs),
                    TP=unlist(pred1@tp), FP=unlist(pred1@fp),
                    FN=unlist(pred1@fn), TN=unlist(pred1@tn),
                    Specificity=unlist(pred1@tn)/(unlist(pred1@fp)+unlist(pred1@tn)),
                    Accuracy=((unlist(pred1@tp)+unlist(pred1@tn))/nrow(train_)))

#table1
max(table1$Accuracy)
t1<-which.max(table1$Accuracy)
#t1
kk1<-table1$Cutoff[t+1]

a2<-predict(ansaic,newdata=test_,type="response")
aa2<-data.frame(a2,test_[1])
pred2<- prediction(aa2[,1], aa2[,2])
perf2 <- performance(pred2, "tpr", "fpr")
plot(perf2)
table2 <- data.frame(Cutoff=unlist(pred2@cutoffs),
                     TP=unlist(pred2@tp), FP=unlist(pred2@fp),
                     FN=unlist(pred2@fn), TN=unlist(pred2@tn),
                     Sensitivity=unlist(pred2@tp)/(unlist(pred2@tp)+unlist(pred2@fn)),
                     Specificity=unlist(pred2@tn)/(unlist(pred2@fp)+unlist(pred2@tn)),
                     Accuracy=((unlist(pred2@tp)+unlist(pred2@tn))/nrow(test_))
)
#table2
auc.tmp<- performance(pred2,"auc")
auc <- as.numeric(auc.tmp@y.values)



aic.fit<-ceiling(predict(ansaic,newdata=test_,type="response")-kk)
aic1.fit<-ceiling(predict(ansaic,newdata=test_,type="response")-0.5)
aic2.fit<-ceiling(predict(ansaic,newdata=test_,type="response")-kk1)

pre<-table(data.frame(test_[1],aic.fit))
pre1<-table(data.frame(test_[1],aic1.fit))
pre2<-table(data.frame(test_[1],aic2.fit))
df<-0.0
df1<-0.0
df2<-0.0

pro<-data.frame(test[77],test_[1],aic.fit,aic1.fit,aic2.fit)

for (x in 1:nrow(pro)){ 
  if (pro[x,3]==1 && pro[x,2]==1)
    df<-df+pro[x,1]
}

for (y in 1:nrow(pro)){ 
  if (pro[y,4]==1 && pro[y,2]==1)
    df1<-df1+pro[y,1]
}

for (z in 1:nrow(pro)){ 
  if (pro[z,5]==1 && pro[z,2]==1)
    df2<-df2+pro[z,1]
}
summary(ans)
summary(ansaic)
vif(ans)
pre#0816 17 18
pre1#0.5
#pre2

#exp(coef(ansaic))

(sum(diag(pre))/sum(pre)) #的中率0816 17 18
(sum(diag(pre1))/sum(pre1)) #的中率0.5
#(sum(diag(pre2))/sum(pre2))*100 #的中率0816 0816 18

df/((pre[1,2]+pre[2,2])*100)#回収率0816 17 18
df1/((pre1[1,2]+pre1[2,2])*100)#回収率0.5
#df2/((pre2[1,2]+pre2[2,2])*100)*100#回収率0816 0816 18 

AIC(ansaic)
kk #0816 17 18
#kk1 #0816 0816 18
auc



