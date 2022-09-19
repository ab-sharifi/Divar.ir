using System.ComponentModel.DataAnnotations;

namespace Divar.Data.Models
{
    public class Users
    {
        [Key]
        public int Id { get; set; }

        [Display(Name = "نام کاربری")]
        [Required(ErrorMessage = "لطفا {0} را به درستی وارد کنید")]
        [MaxLength(80, ErrorMessage = "تعداد حروف بیشتر از حد مجاز است")]
        [MinLength(3, ErrorMessage = "تعداد حروف کمتر از حد مجاز است")]
        public string UserName { get; set; }

        [Display(Name = "کلمه عبور")]
        [DataType(DataType.Password)]
        [Required(ErrorMessage = "لطفا {0} را به درستی وارد کنید")]
        [MaxLength(150, ErrorMessage = "تعداد حروف بیشتر از حد مجاز است")]
        [MinLength(6, ErrorMessage = "تعداد حروف کمتر از حد مجاز است")]
        public string Password { get; set; }

        [Display(Name = "ایمیل")]
        [DataType(DataType.EmailAddress, ErrorMessage = "لطفا {0} را با دقت وارد کنید")]
        [Required(ErrorMessage = "لطفا {0} را به درستی وارد کنید")]
        [MaxLength(200, ErrorMessage = "تعداد حروف بیشتر از حد مجاز است")]
        public string Email { get; set; }

        [Display(Name = "شماره تلفن")]
        [DataType(DataType.PhoneNumber, ErrorMessage = "لطفا {0} را با دقت وارد کنید")]
        [Required(ErrorMessage = "لطفا {0} را به درستی وارد کنید")]
        [MaxLength(11, ErrorMessage = "تعداد حروف بیشتر از حد مجاز است")]
        [MinLength(11, ErrorMessage = "تعداد حروف کمتر از حد مجاز است")]
        public string Phone { get; set; }
        public bool isActive { get; set; }

        [Display(Name = "تاریخ ایجاد")]
        [DataType(DataType.DateTime)]
        public DateTime CreateDate { get; set; }

        public virtual IEnumerable<Posts> Posts { get; set; }
        public virtual IEnumerable<VisitHistory> VisitHistory { get; set; }
        public virtual IEnumerable<HistoryLog> HistoryLog { get; set; }
        public virtual IEnumerable<Notes> Notes { get; set; }
        public virtual Cities Cities { get; set; }
    }
}
