#C594 Project 

#correlation matrix and plots
summary(clean.data)
cor(clean.data)
pairs(clean.dataa)

#checking for outliers 
quantile(clean.data$nCommits, probs= c(.95,.975,.99,.995))
#remove unusal values
clean.data1 <- clean.data[which(clean.data$nCommits < 2000),]
summary(clean.data)
#observe data after removing outliers
pairs(clean.data1)

#PCA

X <- clean.data # skip the Status label in the first variable
n <- nrow(X)
p <- ncol(X)

#########################################
#### Principal Component Projections ####
#########################################

# Calculates eigenvalues and eigenvectors for the covariance matrix
e <- eigen(cov(X))

# Projected data
Y <- (scale(X,center=T,scale=F)) %*% e$vectors 

par(mfrow=c(2,3))
plot(Y[,1],Y[,2],pch=c(rep(1,100),rep(3,100)),
     col=c(rep("blue",100),rep("red",100)),
     main="PC2 vs. PC1",
     xlab="PC1",ylab="PC2")
plot(Y[,2],Y[,3],pch=c(rep(1,100),rep(3,100)),
     col=c(rep("blue",100),rep("red",100)),
     main="PC3 vs. PC2",
     xlab="PC2",ylab="PC3")
plot(Y[,1],Y[,3],pch=c(rep(1,100),rep(3,100)),
     col=c(rep("blue",100),rep("red",100)),
     main="PC3 vs. PC1",
     xlab="PC1",ylab="PC3")
barplot(e$vectors[,1],names.arg=paste("X",1:33,sep=""),
        main="Coefficients for PC1",xlab="",ylab="Eigenvector 1")
barplot(e$vectors[,2],names.arg=paste("X",1:33,sep=""),
        main="Coefficients for PC2",xlab="",ylab="Eigenvector 2")
barplot(e$vectors[,3],names.arg=paste("X",1:33,sep=""),
        main="Coefficients for PC3",xlab="",ylab="Eigenvector 3")
dev.off()

#####################################################
#### Scree Plot to Visualize Variation Explained ####
#####################################################

barplot(e$values,names.arg=1:6,xlab="Index",ylab="Lambda")
plot(e$values/sum(e$values),type="o",xlab="Index",ylab="Variation Explained")
