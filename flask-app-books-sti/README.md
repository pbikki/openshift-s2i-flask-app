# Source-To-Image (S2I)

Source-to-Image (S2I) is a toolkit and workflow for building reproducible container images from source code. S2I produces ready-to-run images by injecting source code into a container image and letting the container prepare that source code for execution. By creating self-assembling builder images, you can version and control your build environments exactly like you use container images to version your runtime environments.

### Build image locally 
Download the [latest release](https://github.com/openshift/source-to-image/releases/tag/v1.2.0)

```
$ s2i build https://github.com/poojitha-bikki/openshift-s2i.git  centos/python-36-centos7 s2i-books-flask-app:v0 --context-dir=/flask-app-books-sti/books-app-src --ref=master
```
The flags used in the above command:
```
--context-dir string               Specify the sub-directory inside the repository with the application sources
--ref string                       Specify a ref to check-out from the supplied git repo
```

https://docs.okd.io/latest/dev_guide/builds/build_strategies.html#source-to-image-strategy-options


oc create -f buildconfig.yaml
```
oc new-app https://github.com/poojitha-bikki/openshift-s2i-flask-app.git --context-dir=/flask-app-books-sti/books-app-src

--> Creating resources ...
    imagestream.image.openshift.io "openshift-s2i-flask-app" created
    buildconfig.build.openshift.io "openshift-s2i-flask-app" created
    deploymentconfig.apps.openshift.io "openshift-s2i-flask-app" created
    service "openshift-s2i-flask-app" created

```
oc start-build flask-app-books-s2i-bc --follow

oc create imagestream flask-app-books-s2i-is

oc logs -f bc/flask-app-books-s2i-bc 