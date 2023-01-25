//refs
void enable_shift();
void disable_shift();
int check_shift();
void enable_ctrl();
void disable_ctrl();
int check_ctrl();
void enable_caps();
void disable_caps();
int check_caps();
void enable_alt();
void disable_alt();
int check_alt();
void keyboard_handler(struct regs *r);
void keyboard_install();