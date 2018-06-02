

#ifndef MY_MODULE_H__
#define MY_MODULE_H__

#ifdef __cplusplus
extern "C" {
#endif

    void MyModule_SayHello(const char name[]);
    void MyModule_SayGoodbye(void);

#ifdef __cplusplus
};
#endif

#endif /*MY_MODULE_H__*/
