/* Portions Copyright (c) 2005-2006 Nokia Corporation */

/* File object interface */

#ifndef Py_FILEOBJECT_H
#define Py_FILEOBJECT_H
#ifdef __cplusplus
extern "C" {
#endif

  /* extern DL_IMPORT(const PyTypeObject) PyFile_Type; */

#define PyFile_Type ((PYTHON_GLOBALS->tobj).t_PyFile)

#define PyFile_Check(op) PyObject_TypeCheck(op, &PyFile_Type)
#define PyFile_CheckExact(op) ((op)->ob_type == &PyFile_Type)

extern DL_IMPORT(PyObject *) PyFile_FromString(char *, char *);
extern DL_IMPORT(void) PyFile_SetBufSize(PyObject *, int);
extern DL_IMPORT(PyObject *) PyFile_FromFile(FILE *, char *, char *,
                                             int (*)(FILE *));
extern DL_IMPORT(FILE *) PyFile_AsFile(PyObject *);
extern DL_IMPORT(PyObject *) PyFile_Name(PyObject *);
extern DL_IMPORT(PyObject *) PyFile_GetLine(PyObject *, int);
extern DL_IMPORT(int) PyFile_WriteObject(PyObject *, PyObject *, int);
extern DL_IMPORT(int) PyFile_SoftSpace(PyObject *, int);
extern DL_IMPORT(int) PyFile_WriteString(const char *, PyObject *);
extern DL_IMPORT(int) PyObject_AsFileDescriptor(PyObject *);

/* The default encoding used by the platform file system APIs
   If non-NULL, this is different than the default encoding for strings
*/
#ifdef __EABI__
extern const char * const Py_FileSystemDefaultEncoding;
#else
extern DL_IMPORT(const char * const) Py_FileSystemDefaultEncoding;
#endif


#ifdef __cplusplus
}
#endif
#endif /* !Py_FILEOBJECT_H */
