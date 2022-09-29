OBS_PROJECT := EA4-experimental
DISABLE_BUILD := arch=i586
scl-php74-snuffleupagus-obs : DISABLE_BUILD += repository=CentOS_9
scl-php73-snuffleupagus-obs : DISABLE_BUILD += repository=CentOS_9
scl-php72-snuffleupagus-obs : DISABLE_BUILD += repository=CentOS_9
scl-php71-snuffleupagus-obs : DISABLE_BUILD += repository=CentOS_8 repository=CentOS_9
scl-php70-snuffleupagus-obs : DISABLE_BUILD += repository=CentOS_8 repository=CentOS_9
include $(EATOOLS_BUILD_DIR)obs-scl.mk
