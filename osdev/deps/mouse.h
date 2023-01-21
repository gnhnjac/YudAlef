//refs
void mouse_wait(uint8_t type);
void mouse_handler(struct regs *r);
void ack();
void mouse_write(uint8_t byte);
void mouse_install();