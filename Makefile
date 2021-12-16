OBS_PROJECT := EA4-experimental
DISABLE_BUILD := arch=i586
scl-php71-snuffleupagus-obs : DISABLE_BUILD += repository=CentOS_8
scl-php70-snuffleupagus-obs : DISABLE_BUILD += repository=CentOS_8
include $(EATOOLS_BUILD_DIR)obs-scl.mk
