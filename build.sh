# build and push image to docker hub
docker build --tag cebox616/copl_store_comics:1.0 .
docker push cebox616/copl_store_comics:1.0
docker rmi cebox616/copl_store_comics:1.0
