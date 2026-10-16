// Thin adapter for installed GzsTool.Core 0.5.3 (Atvaark), not an archive codec.
// PFTXS framing follows upstream fc4a8196555638c6cf8aa1b7c8dc34ccd5c69cb5:
// PftxsFile.cs32-50 / PftxsFtexFile.cs38-66; entry tables use public entry.Read.
// See THIRD-PARTY-NOTICES.txt for Atvaark's MIT notice.
using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Reflection;
using System.Security.Cryptography;
using System.Text;
using GzsTool.Core.Qar;
using GzsTool.Core.Fpk;
using GzsTool.Core.Pftxs;
using GzsTool.Core.Sbp;
using GzsTool.Core.Utility;

public class EntryPoint {
    public static int Main(string[] args) {
        try {
            string root = args[4];
            AppDomain.CurrentDomain.AssemblyResolve += delegate(object s, ResolveEventArgs e) {
                string p = Path.Combine(root, new AssemblyName(e.Name).Name + ".dll");
                return File.Exists(p) ? Assembly.LoadFrom(p) : null;
            };
            foreach (string n in new [] {"CityHash.dll", "Zlib.Portable.dll", "GzsTool.Core.dll"})
                Assembly.LoadFrom(Path.Combine(root,n));
            return ArchiveBridge.Run(args);
        } catch(Exception e) { Console.Error.WriteLine(e.ToString()); return 1; }
    }
}
public class MeteredStream : Stream {
    readonly Stream inner; readonly long limit;
    public long BytesRead;
    public MeteredStream(Stream s, long b) { inner=s;limit=b; }
    public override int Read(byte[] b,int o,int n) {
        if(n<0 || n>limit-BytesRead) throw new InvalidDataException("io_budget");
        int k=inner.Read(b,o,n);BytesRead+=k;return k;
    }
    public override int ReadByte() { byte[] a=new byte[1]; return Read(a,0,1)==0?-1:a[0]; }
    public override long Seek(long x,SeekOrigin origin) {
        long p=origin==SeekOrigin.Begin?x:origin==SeekOrigin.Current?Position+x:Length+x;
        if(p<0 || p>Length) throw new InvalidDataException("seek_outside_container");
        return inner.Seek(p,SeekOrigin.Begin);
    }
    public override bool CanRead {get{return true;}}
    public override bool CanSeek {get{return true;}}
    public override bool CanWrite {get{return false;}}
    public override long Length {get{return inner.Length;}}
    public override long Position {get{return inner.Position;}set{Seek(value,SeekOrigin.Begin);}}
    public override void Flush(){}
    public override void SetLength(long x){throw new NotSupportedException();}
    public override void Write(byte[] b,int o,int n){throw new NotSupportedException();}
    protected override void Dispose(bool d){if(d)inner.Dispose();base.Dispose(d);}
}
public class TextureEntry {
    public PftxsFtexsFileEntry Entry; public long AbsoluteOffset;
}
public static class ArchiveBridge {
    static MeteredStream active; static long decoded; static int maxMembers;
    static Dictionary<string,object> Row(params object[] a) {
        var d=new Dictionary<string,object>();for(int i=0;i<a.Length;i+=2)d[(string)a[i]]=a[i+1];return d;
    }
    static string Quote(string s) {
        if(s==null)return "null";
        var b=new StringBuilder("\""); foreach(char c in s) {
            if(c=='"')b.Append("\\\"");else if(c=='\\')b.Append("\\\\");
            else if(c<32)b.Append("\\u"+((int)c).ToString("x4"));else b.Append(c);
        } return b.Append('"').ToString();
    }
    static string Json(object x) {
        if(x==null)return "null";if(x is string)return Quote((string)x);
        if(x is bool)return (bool)x?"true":"false";
        var d=x as IDictionary;if(d!=null){var a=new List<string>();foreach(DictionaryEntry p in d)a.Add(Quote((string)p.Key)+":"+Json(p.Value));return "{"+String.Join(",",a.ToArray())+"}";}
        var en=x as IEnumerable;if(en!=null){var a=new List<string>();foreach(object p in en)a.Add(Json(p));return "["+String.Join(",",a.ToArray())+"]";}
        return Convert.ToString(x,System.Globalization.CultureInfo.InvariantCulture);
    }
    static void WriteJson(string path,object x) {File.WriteAllText(path,Json(x),new UTF8Encoding(false));}
    static void Bounds(long offset,long size,Stream s) {
        if(offset<0||size<0||offset>s.Length||size>s.Length-offset)throw new InvalidDataException("member_outside_container");
    }
    static void Count(long n){if(n<0||n>maxMembers)throw new InvalidDataException("member_limit");}
    static string Ext(string name) {
        if(String.IsNullOrEmpty(name))return "_unknown";
        string n=name.Replace('\\','/');int dot=n.LastIndexOf('.');
        if(dot<0)return "_unknown";
        if(n.EndsWith(".ftexs",StringComparison.OrdinalIgnoreCase)&&dot>=2&&n[dot-2]=='.'&&Char.IsDigit(n[dot-1]))return n.Substring(dot-1).ToLowerInvariant();
        return n.Substring(dot+1).ToLowerInvariant();
    }
    static string ExtHash(ulong hash) {
        foreach(string ext in new[]{"ftex","1.ftexs","2.ftexs","3.ftexs","4.ftexs","5.ftexs","6.ftexs","fpk","fpkd","pftxs","sbp","dat"})
            if((Hashing.HashFileNameWithExtension("/Assets/catalogue."+ext)>>51)==(hash>>51))return ext;
        return "_unknown";
    }
    static void Preflight(string kind,Stream s) {
        s.Position=0;var b=new BinaryReader(s,Encoding.ASCII,true);
        if(kind=="qar"){
            if(!QarFile.IsQarFile(s))throw new InvalidDataException("not_sqar");
            s.Position=8;uint n=b.ReadUInt32()^0x11C22050U;uint unknown=b.ReadUInt32()^0xD05608C3U;
            Count(n);Count(unknown);Bounds(32,8L*n+16L*unknown,s);
        } else if(kind=="fpk"||kind=="fpkd"){
            Bounds(0,48,s);byte[] h=b.ReadBytes(6);
            if(Encoding.ASCII.GetString(h)!="foxfpk")throw new InvalidDataException("not_fpk");
            s.Position=36;uint n=b.ReadUInt32(),r=b.ReadUInt32();Count(n);Count(r);Bounds(48,48L*n+16L*r,s);
        } else if(kind=="sbp"){
            Bounds(0,8,s);if(b.ReadUInt32()!=0x4c504253U)throw new InvalidDataException("not_sbp");
            int n=b.ReadByte();Bounds(8,n*12L,s);
        }
        s.Position=0;
    }
    static List<TextureEntry> TextureIndex(Stream s) {
        s.Position=0;var r=new BinaryReader(s,Encoding.ASCII,true);
        Bounds(0,32,s);if(r.ReadUInt32()!=0x58544650U)throw new InvalidDataException("not_pftxs");
        s.Position=16;if(r.ReadUInt32()!=0x4c584554U)throw new InvalidDataException("not_texl");
        int size=r.ReadInt32(),count=r.ReadInt32();r.ReadInt32();Count(count);Bounds(16,size,s);
        var all=new List<TextureEntry>();
        for(int i=0;i<count;i++){
            long start=s.Position;Bounds(start,32,s);
            if(r.ReadUInt32()!=0x58455446U)throw new InvalidDataException("not_texture_block");
            int blockSize=r.ReadInt32();r.ReadUInt64();int n=r.ReadInt32();r.ReadBytes(12);
            Count(n);Bounds(start,blockSize,s);if(blockSize<32L+16L*n)throw new InvalidDataException("short_texture_table");
            for(int j=0;j<n;j++){
                var e=new PftxsFtexsFileEntry();e.Read(s);
                if(e.Offset<32L+16L*n||e.Size<0||e.Offset>blockSize||e.Size>blockSize-e.Offset)throw new InvalidDataException("texture_range");
                all.Add(new TextureEntry{Entry=e,AbsoluteOffset=start+e.Offset});Count(all.Count);
            }
            s.Position=start+blockSize;
        } return all;
    }
    static int Index(string kind,string name,string output) {
        int ordinal=0;using(var w=new StreamWriter(output,false,new UTF8Encoding(false))){
            if(kind=="qar"){
                var q=new QarFile();q.Read(active);
                foreach(var e in q.Entries){Bounds(e.DataOffset,e.UncompressedSize,active);
                    w.WriteLine(Json(Row("record","member","ordinal",ordinal++,"name",e.FilePath,"name_origin",e.FileNameFound?"dictionary":"hash_fallback","resolved",e.FileNameFound,"hash",e.Hash.ToString("x16"),"path_hash",(e.Hash&0x3ffffffffffffUL).ToString("x"),"extension_id",(e.Hash>>51).ToString(),"extension",Ext(e.FilePath),"offset",e.DataOffset,"declared_size",e.UncompressedSize,"compressed_size",e.CompressedSize,"compressed",e.Compressed,"meta_flag",e.MetaFlag)));}
            }else if(kind=="fpk"||kind=="fpkd"){
                var p=new FpkFile();p.Read(active);
                foreach(var e in p.Entries){Bounds(e.DataOffset,e.DataSize,active);var n=e.FilePathFpkString;
                    w.WriteLine(Json(Row("record","member","ordinal",ordinal++,"name",e.FilePath,"name_origin",n.ValueEncrypted?(n.ValueResolved?"dictionary":"hash_fallback"):"embedded","resolved",n.ValueResolved,"hash",null,"filename_md5",BitConverter.ToString(e.Md5Hash).Replace("-","").ToLowerInvariant(),"encrypted_name_base64",n.EncryptedValue==null?null:Convert.ToBase64String(n.EncryptedValue),"extension",Ext(e.FilePath),"offset",e.DataOffset,"declared_size",e.DataSize)));}
                int refIndex=0;foreach(var r in p.References)w.WriteLine(Json(Row("record","reference","ordinal",refIndex++,"name",r.FilePath,"name_origin","embedded")));
            }else if(kind=="sbp"){
                var p=new SbpFile{Name=name};p.Read(active);
                foreach(var e in p.Entries){Bounds(e.Offset,e.Size,active);w.WriteLine(Json(Row("record","member","ordinal",ordinal++,"name",e.FileName,"name_origin","generated","resolved",false,"extension",Ext(e.FileName),"offset",e.Offset,"declared_size",e.Size)));}
            }else if(kind=="pftxs"){
                foreach(var t in TextureIndex(active)){var e=t.Entry;string ext=ExtHash(e.Hash);
                    w.WriteLine(Json(Row("record","member","ordinal",ordinal++,"name",e.Hash.ToString("x16")+"."+ext,"name_origin","hash_fallback","resolved",false,"hash",e.Hash.ToString("x16"),"extension_id",(e.Hash>>51).ToString(),"extension",ext,"offset",t.AbsoluteOffset,"declared_size",e.Size)));}
            }else throw new InvalidDataException("unsupported_container");
        }return ordinal;
    }
    static void Export(string kind,string name,int ordinal,string output,long maxBytes) {
        Func<Stream> data=null;
        if(kind=="qar"){var q=new QarFile();q.Read(active);if(ordinal<0||ordinal>=q.Entries.Count)throw new InvalidDataException("ordinal");
            var e=q.Entries[ordinal];if(e.UncompressedSize>maxBytes||e.CompressedSize>maxBytes)throw new InvalidDataException("container_budget");
            data=e.Export(active).DataStream;
        }else if(kind=="fpk"||kind=="fpkd"){var p=new FpkFile();p.Read(active);if(ordinal<0||ordinal>=p.Entries.Count)throw new InvalidDataException("ordinal");
            var e=p.Entries[ordinal];if(e.DataSize>maxBytes)throw new InvalidDataException("container_budget");data=e.Export(active).DataStream;
        }else if(kind=="sbp"){var p=new SbpFile{Name=name};p.Read(active);if(ordinal<0||ordinal>=p.Entries.Count)throw new InvalidDataException("ordinal");
            var e=p.Entries[ordinal];if(e.Size>maxBytes)throw new InvalidDataException("container_budget");data=e.Export(active).DataStream;
        }else if(kind=="pftxs"){
            var entries=TextureIndex(active);if(ordinal<0||ordinal>=entries.Count)throw new InvalidDataException("ordinal");var t=entries[ordinal];
            if(t.Entry.Size>maxBytes)throw new InvalidDataException("container_budget");
            using(var dest=new FileStream(output,FileMode.CreateNew,FileAccess.Write)){active.Position=t.AbsoluteOffset;byte[] b=new byte[65536];long remain=t.Entry.Size;
                while(remain>0){int n=active.Read(b,0,(int)Math.Min(remain,b.Length));if(n==0)throw new EndOfStreamException();dest.Write(b,0,n);remain-=n;}decoded=dest.Length;}
            return;
        }else throw new InvalidDataException("unsupported_container");
        using(Stream payload=data()){decoded=payload.Length;if(decoded>maxBytes)throw new InvalidDataException("decoded_container_budget");
            using(var dest=new FileStream(output,FileMode.CreateNew,FileAccess.Write))payload.CopyTo(dest);}
    }
    public static int Run(string[] a) {
        string action=a[0],kind=a[1],source=a[2],output=a[3],tool=a[4],name=a[6];
        int ordinal=Int32.Parse(a[5]);long maxBytes=Int64.Parse(a[7]),maxRead=Int64.Parse(a[8]);maxMembers=Int32.Parse(a[9]);
        int count=0,code=0;string error=null;long dictionaryBytes=0;
        try {
            dictionaryBytes=new FileInfo(Path.Combine(tool,"qar_dictionary.txt")).Length+new FileInfo(Path.Combine(tool,"fpk_dictionary.txt")).Length;
            if(dictionaryBytes>maxRead)throw new InvalidDataException("dictionary_io_budget");
            Hashing.ReadDictionary(Path.Combine(tool,"qar_dictionary.txt"));Hashing.ReadMd5Dictionary(Path.Combine(tool,"fpk_dictionary.txt"));
            using(active=new MeteredStream(new FileStream(source,FileMode.Open,FileAccess.Read,FileShare.Read),maxRead-dictionaryBytes)){
                Preflight(kind,active);
                if(action=="index")count=Index(kind,name,output);else if(action=="extract")Export(kind,name,ordinal,output,maxBytes);else throw new InvalidDataException("action");
            }
        }catch(Exception e){code=1;error=e.GetType().Name+": "+e.Message;Console.Error.WriteLine(error);}
        WriteJson(output+".receipt.json",Row("ok",code==0,"action",action,"kind",kind,"member_count",count,"read_bytes",dictionaryBytes+(active==null?0:active.BytesRead),"decoded_bytes",decoded,"payload_decode_requested",action=="extract","error",error));
        return code;
    }
}
