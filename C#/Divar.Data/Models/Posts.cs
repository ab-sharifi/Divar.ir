using System.ComponentModel.DataAnnotations;

namespace Divar.Data.Models
{
    public class Posts
    {
        [Key]
        public int Id { get; set; }
        public int UserId { get; set; }

        [Display(Name = "عنوان آگهی")]
        [Required(ErrorMessage = "لطفا {0} را به درستی وارد کنید")]
        [MaxLength(100, ErrorMessage = "تعداد حروف بیشتر از حد مجاز است")]
        [MinLength(10, ErrorMessage = "تعداد حروف کمتر از حد مجاز است")]
        public string PostTitle { get; set; }

        [Display(Name = "شرح آگهی")]
        [Required(ErrorMessage = "لطفا {0} را به درستی وارد کنید")]
        [MaxLength(500, ErrorMessage = "تعداد حروف بیشتر از حد مجاز است")]
        [MinLength(50, ErrorMessage = "تعداد حروف کمتر از حد مجاز است")]
        public string PostCaption { get; set; }

        [Display(Name = "تصویر آگهی")]
        [DataType(DataType.Upload)]
        public string ImageLocation { get; set; }

        [Display(Name = "قیمت آگهی")]
        [Required(ErrorMessage = "لطفا {0} را به درستی وارد کنید")]
        [DataType(DataType.Currency)]
        public string PostPrice { get; set; }

        [Display(Name = "دسته‌بندی آگهی")]
        public string PostCategories { get; set; }

        [Display(Name = "وضعیت آگهی")]
        public bool PostStatus { get; set; }

        [Display(Name = "آخرین بروزرسانی")]
        [DataType(DataType.DateTime)]
        public DateTime LastUpdate { get; set; }

        [Display(Name = "تاریخ ایجاد")]
        [DataType(DataType.DateTime)]
        public DateTime CreateDate { get; set; }


        public virtual Users Users { get; set; }
        public virtual IEnumerable<Categories> Categories { get; set; }
        public virtual IEnumerable<Notes> Notes { get; set; }
        public virtual IEnumerable<VisitHistory> VisitHistory { get; set; }
        public virtual IEnumerable<HistoryLog> HistoryLog { get; set; }
    }
}
