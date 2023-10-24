# add 

CPP_SOURCES = \
User/Src/User_main.cpp

ifdef GCC_PATH
CXX = $(GCC_PATH)/$(PREFIX)g++
else
CXX = $(PREFIX)g++
endif

# Cpp includes
# 在这里添加所需的CPP头文件即可，与C共用同一个
C_INCLUDES =  \
-IUser/Inc

# AS includes
AS_INCLUDES =  \
-ICore/Inc \
-IUser/Inc

# compile gcc flags
CPPFLAGS = $(MCU) $(C_DEFS) $(C_INCLUDES) $(OPT) -Wall -fdata-sections -ffunction-sections

ifeq ($(DEBUG), 1)
CFLAGS += -g -gdwarf-2
CPPFLAGS += -g -gdwarf-2
endif

CPPFLAGS += -MMD -MP -MF"$(@:%.o=%.d)"

#######################################
# LDFLAGS
#######################################
# link script
# 增添  -specs=nosys.specs
LDFLAGS = $(MCU) -specs=nano.specs -specs=nosys.specs -T$(LDSCRIPT) $(LIBDIR) $(LIBS) -Wl,-Map=$(BUILD_DIR)/$(TARGET).map,--cref -Wl,--gc-sections

# build the application
CPP_OBJECTS = $(addprefix $(BUILD_DIR)/, $(notdir $(CPP_SOURCES:.cpp=.o)))
vpath %.cpp $(sort $(dir $(CPP_SOURCES)))

# 这一句添加CPP_OBJECTS 到总 OBJECTS
OBJECTS += $(CPP_OBJECTS)


# 编译器选择
# c文件使用gcc编译，  cpp文件使用g++编译，最后统一使用g++链接 
$(BUILD_DIR)/%.o: %.c Makefile | $(BUILD_DIR) 
	$(CC) -c $(CFLAGS) -Wa,-a,-ad,-alms=$(BUILD_DIR)/$(notdir $(<:.c=.lst)) $< -o $@
# add
$(BUILD_DIR)/%.o: %.cpp Makefile | $(BUILD_DIR)
	$(CXX) -c $(CPPFLAGS) -Wa,-a,-ad,-alms=$(BUILD_DIR)/$(notdir $(<:.cpp=.lst)) $< -o $@

$(BUILD_DIR)/%.o: %.s Makefile | $(BUILD_DIR)
	$(AS) -c $(CFLAGS) $< -o $@

$(BUILD_DIR)/$(TARGET).elf: $(OBJECTS) Makefile
	$(CXX) $(OBJECTS) $(LDFLAGS) -o $@
	$(SZ) $@

