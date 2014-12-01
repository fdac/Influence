require(gbm)
require(randomForest)
require(rjson)
require(devtools)
source_gist(4676064)

setwd('~/Google Drive/UTK/Fall 2014/COSC 594/Final Project/Influence/data')

nFollowers <- fromJSON(file='nFollowers.data')
fqCommits <- fromJSON(file='fqCommits.data')
nCommits <- fromJSON(file='nCommits.data')
nForks <- fromJSON(file='nForks.data')
nPulls <- fromJSON(file='nPulls.data')
timeContrb <- fromJSON(file='timeContrb.data')
totalRepos <- fromJSON(file='totalRepos.data')
nWatchers <- fromJSON(file='nWatchers.data')

nFollowers2 <- as.data.frame.list(nFollowers)
names(nFollowers2) <- 'nFollowers'
nFollowers2$nFollowers <- log(nFollowers2$nFollowers)
nFollowers2$user <- rownames(nFollowers2)
rownames(nFollowers2) <- NULL

fqCommits2 <- as.data.frame.list(fqCommits)
names(fqCommits2) <- 'fqCommits'
fqCommits2$user <- rownames(fqCommits2)
rownames(fqCommits2) <- NULL

nCommits2 <- as.data.frame.list(nCommits)
names(nCommits2) <- 'nCommits'
nCommits2$user <- rownames(nCommits2)
rownames(nCommits2) <- NULL

nForks2 <- as.data.frame.list(nForks)
names(nForks2) <- 'nForks'
nForks2$user <- rownames(nForks2)
rownames(nForks2) <- NULL

nPulls2 <- as.data.frame.list(nPulls)
names(nPulls2) <- 'nPulls'
nPulls2$user <- rownames(nPulls2)
rownames(nPulls2) <- NULL

timeContrb2 <- as.data.frame.list(timeContrb)
names(timeContrb2) <- 'timeContrb'
timeContrb2$user <- rownames(timeContrb2)
rownames(timeContrb2) <- NULL

totalRepos2 <- as.data.frame.list(totalRepos)
names(totalRepos2) <- 'totalRepos'
totalRepos2$user <- rownames(totalRepos2)
rownames(totalRepos2) <- NULL

nWatchers2 <- as.data.frame.list(nWatchers)
names(nWatchers2) <- 'nWatchers'
nWatchers2$user <- rownames(nWatchers2)
rownames(nWatchers2) <- NULL

tmp1 <- merge(nWatchers2, fqCommits2, all=T)
tmp2 <- merge(tmp1, nCommits2, all=T)
tmp3 <- merge(tmp2, nForks2, all=T)
tmp4 <- merge(tmp3, nPulls2, all=T)
tmp5 <- merge(tmp4, timeContrb2, all=T)
data <- merge(tmp5, totalRepos2, all=T)
rownames(data) <- data[,1]
data <- data[,-1]
data <- data[complete.cases(data$nWatchers),]
#data$nFollowers[which(is.na(data$nFollowers))] <- 0
#data$nForks[which(is.na(data$nForks))] <- 0
#data$nPulls[which(is.na(data$nPulls))] <- 0
#data$fqCommits[which(is.na(data$fqCommits))] <- 0
#data$nCommits[which(is.na(data$nCommits))] <- 0
#data$timeContrb[which(is.na(data$timeContrb))] <- 0
#data$totalRepos[which(is.na(data$totalRepos))] <- 0

### train and test sets
idx <- sample(1:nrow(data), floor(.7*nrow(data)))
train <- data[idx,]
#train <- rbind(sample(zero, 100000), data[sample(nonzero, 200000, replace=T),])


xtrain <- train[,-1]
ytrain <- train[,1]

test <- data[-idx,]
xtest <- test[,-1]
ytest <- test[,1]

length(data[complete.cases(data),])
dim(data)

### GBM
gbmod <- gbm.fit(x=xtrain, y=ytrain, distribution='gaussian')
pred <- predict(gbmod, xtest, n.trees=100)

forplot <- data.frame(ytest, pred)
require(ggplot2)
p <- ggplot(forplot, aes(pred, ytest))
p <- p + geom_point(alpha=.5)
p
