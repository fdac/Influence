require(gbm)
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

nFollowers2 <- as.data.frame(nFollowers)
names(nFollowers2) <- 'nFollowers'
nFollowers2$nFollowers <- log(nFollowers2$nFollowers)
nFollowers2$user <- rownames(nFollowers2)
rownames(nFollowers2) <- NULL

fqCommits2 <- as.data.frame(fqCommits)
names(fqCommits2) <- 'fqCommits'
fqCommits2$user <- rownames(fqCommits2)
rownames(fqCommits2) <- NULL

nCommits2 <- as.data.frame(nCommits)
names(nCommits2) <- 'nCommits'
nCommits2$user <- rownames(nCommits2)
rownames(nCommits2) <- NULL

nForks2 <- as.data.frame(nForks)
names(nForks2) <- 'nForks'
nForks2$user <- rownames(nForks2)
rownames(nForks2) <- NULL

nPulls2 <- as.data.frame(nPulls)
names(nPulls2) <- 'nPulls'
nPulls2$user <- rownames(nPulls2)
rownames(nPulls2) <- NULL

timeContrb2 <- as.data.frame(timeContrb)
names(timeContrb2) <- 'timeContrb'
timeContrb2$user <- rownames(timeContrb2)
rownames(timeContrb2) <- NULL

totalRepos2 <- as.data.frame(totalRepos)
names(totalRepos2) <- 'totalRepos'
totalRepos2$user <- rownames(totalRepos2)
rownames(totalRepos2) <- NULL

tmp1 <- merge(nFollowers2, fqCommits2, all=T)
tmp2 <- merge(tmp1, nCommits2, all=T)
tmp3 <- merge(tmp2, nForks2, all=T)
tmp4 <- merge(tmp3, nPulls2, all=T)
tmp5 <- merge(tmp4, timeContrb2, all=T)
data <- merge(tmp5, totalRepos2, all=T)
rownames(data) <- data[,1]
data <- data[,-1]
data$nFollowers[which(is.na(data$nFollowers))] <- 0

### train and test sets
idx <- sample(1:nrow(data), floor(.7*nrow(data)))

train <- data[idx,]
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
