#!/usr/bin/env python
# coding: utf-8

# In[1]:


from math import pi, sin, cos #digunakan untuk menghitung pergerakan kamera
from direct.showbase.ShowBase import ShowBase #untuk mengambil dan menampilkan image dari framework ShowBase. ShowBase juga dapat digunakan untuk memberikan inputan dan gerakan.
from direct.task import Task #manajemen kegiatan/fungsi pada python (event handling)
from direct.actor.Actor import Actor #meload kelas aktor yang digunakan.
from direct.interval.IntervalGlobal import Sequence #memanipulasi waktu/durasi movement pada suatu nilai tertentu
from panda3d.core import Point3 #untuk mengatur koordinat aktor
 
class MyApp(ShowBase):
    def __init__(self): 
        ShowBase.__init__(self) # menginisialisasi modul ShowBase

        # Nonaktifkan kontrol trackball kamera.
        self.disableMouse()

        # load model lingkungan.
        self.scene = self.loader.loadModel("models/environment")
        # Atur ulang model yang akan dirender.
        self.scene.reparentTo(self.render) 
        # Terapkan transformasi skala dan posisi pada model.
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

        # Tambahkan prosedur spinCameraTask ke pengelola tugas.
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

        # Load dan ubah aktor panda.
        self.pandaActor = Actor("models/panda-model",
                                {"walk": "models/panda-walk4"})
        self.pandaActor.setScale(0.005, 0.005, 0.005)
        self.pandaActor.reparentTo(self.render)
        # Putar animasinya.
        self.pandaActor.loop("walk")

        # Buat empat interval lerp yang dibutuhkan panda untuk
        # berjalan maju mundur.
        posInterval1 = self.pandaActor.posInterval(13,
                                                   Point3(0, -10, 0),
                                                   startPos=Point3(0, 10, 0))
        posInterval2 = self.pandaActor.posInterval(13,
                                                   Point3(0, 10, 0),
                                                   startPos=Point3(0, -10, 0))
        hprInterval1 = self.pandaActor.hprInterval(3,
                                                   Point3(180, 0, 0),
                                                   startHpr=Point3(0, 0, 0))
        hprInterval2 = self.pandaActor.hprInterval(3,
                                                   Point3(0, 0, 0),
                                                   startHpr=Point3(180, 0, 0))

        # Buat dan mainkan urutan yang mengoordinasikan interval.
        self.pandaPace = Sequence(posInterval1, hprInterval1,
                                  posInterval2, hprInterval2,
                                  name="pandaPace")
        self.pandaPace.loop()

    # Tentukan prosedur untuk memindahkan kamera.
    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0 #angle degress untuk mencari sudut kamera, sedangkan angleRadians digunakan untuk mendapatkan nilai radian dari sudut kamera tersebut dan task.time mengembalikan nilai (float) yang menunjukkan berapa lama fungsi tugas ini telah berjalan sejak eksekusi pertama fungsi tersebut. Timer berjalan bahkan ketika fungsi tugas tidak dijalankan.  
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 3) #fungsi awal pergerakan kamera dimulai sedangkan setHpr mengembalikan kamera ke koordinat semula
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont

#inisialisasi Function MyApp() ke variabel app
app = MyApp()
#load Musik 
mySound = app.loader.loadSfx("ForestWalk-320bit_1.ogg")
#mutar Musik
mySound.play()
#Membuat Musik terus berulang
mySound.setLoop(True)
#Mengatur volume
mySound.setVolume(13)
#menjalankan aplikasi
app.run()


# In[ ]:




