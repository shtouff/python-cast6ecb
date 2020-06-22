#define PY_SSIZE_T_CLEAN

#include <Python.h>
#include <mcrypt.h>

#define CAST6ECB_ENCRYPT 0
#define CAST6ECB_DECRYPT 1

static MCRYPT td;

static PyObject *
mcrypt_do_cast6ecb(
    const char *key,
    const size_t klen,
    const char *data,
    const size_t dlen,
    const short dencrypt
){
    PyObject *ret;
    char *mdata;
    size_t mdlen, bsize;

    if (mcrypt_generic_init(td, (void *)key, klen, NULL) < 0)
        return PyErr_Format(PyExc_ValueError, "key is invalid");

    bsize = mcrypt_enc_get_block_size(td);

    mdlen = (((dlen - 1) / bsize) + 1) * bsize;
    mdata = PyMem_Malloc(mdlen + 1);
    if (mdata == NULL)
        return PyErr_NoMemory();

    memset(mdata, 0, mdlen);
    memcpy(mdata, data, dlen);

    if (dencrypt == CAST6ECB_ENCRYPT)
        mcrypt_generic(td, mdata, (int)mdlen);
    else
        mdecrypt_generic(td, mdata, (int)mdlen);

    mdata[mdlen] = 0;

    ret = PyBytes_FromStringAndSize(mdata, mdlen);
    PyMem_Free(mdata);

    return ret;
}

static char
cast6ecb_block_size__doc__[] =
"block_size() -> blocksize\n\
\n\
This is the function that report the block size for CAST-256-ECB.\n\
";

static PyObject *
cast6ecb_block_size(
    PyObject *self,
    PyObject *args
){
    return PyLong_FromLong(mcrypt_enc_get_block_size(td));
}

static char
cast6ecb_encrypt__doc__[] =
"encrypt(key, plaintext) -> secret\n\
\n\
This is the CAST-256-ECB encryption function.\n\
";

static PyObject *
cast6ecb_encrypt(
    PyObject *self,
    PyObject *args
){
    char *key;
    Py_ssize_t klen = 0;
    char *plain;
    Py_ssize_t plen = 0;

    if (!PyArg_ParseTuple(args, "s#s#:encrypt", &key, &klen, &plain, &plen))
        return NULL;

    return mcrypt_do_cast6ecb(key, klen, plain, plen, CAST6ECB_ENCRYPT);
}

static char
cast6ecb_decrypt__doc__[] =
"decrypt(key, secret) -> plaintext\n\
\n\
This is the CAST-256-ECB decryption function.\n\
";

static PyObject *
cast6ecb_decrypt(
    PyObject *self,
    PyObject *args
){
    char *key;
    Py_ssize_t klen = 0;
    char *secret;
    Py_ssize_t slen = 0;

    if (!PyArg_ParseTuple(args, "s#s#:decrypt", &key, &klen, &secret, &slen))
        return NULL;

    return mcrypt_do_cast6ecb(key, klen, secret, slen, CAST6ECB_DECRYPT);
}

static PyMethodDef
cast6ecb_methods[] = {
    {"encrypt",  (PyCFunction)cast6ecb_encrypt, METH_VARARGS, cast6ecb_encrypt__doc__},
    {"decrypt",  (PyCFunction)cast6ecb_decrypt, METH_VARARGS, cast6ecb_decrypt__doc__},
    {"block_size",  (PyCFunction)cast6ecb_block_size, METH_NOARGS, cast6ecb_block_size__doc__},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef
cast6ecb_module = {
    PyModuleDef_HEAD_INIT,
    "cast6ecb",   /* name of module */
    NULL,         /* module documentation, may be NULL */
    -1,           /* size of per-interpreter state of the module,
                     or -1 if the module keeps state in global variables. */
    cast6ecb_methods
};

PyMODINIT_FUNC
PyInit_cast6ecb(
    void
){
    td = mcrypt_module_open(MCRYPT_CAST_256, NULL, MCRYPT_ECB, NULL);
    if (td == MCRYPT_FAILED)
        return PyErr_Format(PyExc_RuntimeError, "could not open CAST-256-ECB module");

    return PyModule_Create(&cast6ecb_module);
}
